import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from dotenv import load_dotenv
import os

load_dotenv()

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('container_list')  # Redirige a la página principal
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al usuario a la página de login

class AddStatusView(LoginRequiredMixin, View):
    template_name = 'packages/add_status.html'

    def get(self, request, package_id):
        return render(request, self.template_name, {'package_id': package_id})

    def post(self, request, package_id):
        status = request.POST.get('status')
        delivered = request.POST.get('delivered') == 'on'  # Verifica si el checkbox está marcado

        # Lógica para marcar como entregado si el checkbox está activado
        if delivered:
            response = requests.put(
                f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}/deliver'
            )
            if response.status_code == 404:
                return render(request, self.template_name, {'package_id': package_id, 'error': 'Package not found.'})
            elif response.status_code != 200:
                return render(request, self.template_name, {'package_id': package_id, 'error': 'Failed to mark as delivered.'})

        # Agregar el estado normalmente
        response = requests.post(
            f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/status/',
            json={'package_id': package_id, 'status': status}
        )

        if response.status_code == 200:
            return redirect('view_statuses', package_id=package_id)
        else:
            return render(request, self.template_name, {'package_id': package_id, 'error': 'Failed to add status.'})

class ContainerListView(LoginRequiredMixin, View):
    template_name = 'containers/container_list.html'

    def get(self, request):
        # Obtener la lista de contenedores
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/')
        containers = response.json()

        # Filtrar los contenedores en activos y archivados
        active_containers = [container for container in containers if container.get('active')]
        archived_containers = [container for container in containers if not container.get('active')]

        # Para cada contenedor, obtener los valores de peso y medida volumétrica
        for container in containers:
            response_values = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/getValuesByContainer/{container["id"]}')
            if response_values.status_code == 200:
                values = response_values.json()
                container["total_weight"] = values.get("total_weight", 0)
                container["total_volumetric_measure"] = values.get("total_volumetric_measure", 0)
            else:
                container["total_weight"] = "N/A"
                container["total_volumetric_measure"] = "N/A"

        # Renderizar la plantilla con los datos obtenidos
        return render(request, self.template_name, {
            'active_containers': active_containers,
            'archived_containers': archived_containers,
        })

class ArchiveContainerView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Enviar la solicitud POST al endpoint de FastAPI para archivar el contenedor
        response = requests.post(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/archive/{pk}')

        if response.status_code == 200:
            # Si la respuesta es exitosa, redirigir a la lista de contenedores
            return HttpResponseRedirect(reverse_lazy('container_list'))
        else:
            # Manejar el error si ocurre
            return render(request, 'containers/container_list.html', {
                'error': 'Error archiving container. Please try again.',
            })
        
class ContainerDetailView(LoginRequiredMixin, View):
    template_name = 'containers/container_detail.html'

    def get(self, request, pk):
        # Obtener los detalles del contenedor
        response = requests.get(
            f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/getContainerById/{pk}')
        container = response.json()

        # Obtener el peso total y la medida volumétrica total usando el nuevo endpoint
        response_values = requests.get(
            f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/getValuesByContainer/{pk}')
        if response_values.status_code == 200:
            values = response_values.json()
            total_weight = values.get('total_weight', 'N/A')
            total_volumetric_measure = values.get('total_volumetric_measure', 'N/A')
        else:
            total_weight = 'N/A'
            total_volumetric_measure = 'N/A'

        # Filtrar paquetes
        tracking_id = request.GET.get('tracking_id')
        min_pieces = request.GET.get('min_pieces')
        max_pieces = request.GET.get('max_pieces')
        created_at_str = request.GET.get('created_at')
        package_type = request.GET.get('package_type')
        delivered = request.GET.get('delivered')

        # Obtener los paquetes asociados al contenedor
        response_packages = requests.get(
            f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/getPackagesByContainer/{pk}')

        # Verificar si la respuesta es correcta
        if response_packages.status_code == 200:
            packages = response_packages.json()  # Se espera que esto sea una lista de paquetes
        else:
            packages = []  # Asignar una lista vacía si la respuesta no es válida

        filtered_packages = []

        # Filtrar la lista de paquetes
        for package in packages:
            # Asegurarse de que package sea un diccionario
            if isinstance(package, dict):
                # Convertir la fecha del paquete a dd/mm/aaaa
                package_created_at = datetime.strptime(package.get('created_at', ''), '%Y-%m-%dT%H:%M:%S')
                package_created_at_str = package_created_at.strftime('%d/%m/%Y')

                if tracking_id and package.get('tracking_id') != tracking_id:
                    continue
                if min_pieces:
                    min_pieces = int(min_pieces)
                    if package.get('pieces') < min_pieces:
                        continue
                if max_pieces:
                    max_pieces = int(max_pieces)
                    if package.get('pieces') > max_pieces:
                        continue
                # Convertir la fecha del filtro a dd/mm/aaaa
                if created_at_str:
                    created_at_datetime = datetime.strptime(created_at_str, '%Y-%m-%d')
                    created_at_str_formatted = created_at_datetime.strftime('%d/%m/%Y')
                    if package_created_at_str != created_at_str_formatted:
                        continue
                if package_type and package.get('package_type') != package_type:
                    continue
                if delivered == 'True' and not package.get('delivered'):
                    continue
                if delivered == 'False' and package.get('delivered'):
                    continue
                filtered_packages.append(package)

        # Pasar los valores al template
        return render(request, self.template_name, {
            'container': container,
            'packages': filtered_packages,  # Usa los paquetes filtrados
            'total_weight': total_weight,
            'total_volumetric_measure': total_volumetric_measure,
        })


class ContainerCreateView(LoginRequiredMixin, View):
    template_name = 'containers/container_form.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        identifier_name = request.POST['identifier_name']
        shipment_type = request.POST['shipment_type']

        # Verifica si el nombre del identificador ya existe
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/')
        containers = response.json()

        if any(container['identifier_name'] == identifier_name for container in containers):
            return render(request, self.template_name, {'error': 'The identifier name is already in use.'})

        # Envía la solicitud para crear un nuevo contenedor
        data = {
            'identifier_name': identifier_name,
            'shipment_type': shipment_type
        }

        response = requests.post(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/', json=data)

        if response.status_code == 200:
            return HttpResponseRedirect('/containers/')

        return render(request, self.template_name, {'error': 'Error creating container'})

class CreatePackageView(LoginRequiredMixin, View):
    template_name = 'packages/create_package.html'

    def get(self, request, container_id):
        # Obtener la lista de contenedores para el dropdown
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/')
        containers = response.json()

        return render(request, self.template_name, {
            'container_id': container_id,
            'containers': containers  # Pasar la lista de contenedores al contexto
        })

    def post(self, request, container_id):
        pseudoname = request.POST.get('pseudoname')
        weight = request.POST.get('weight')
        volumetric_measure = request.POST.get('volumetric_measure')
        pieces= request.POST.get('pieces')
        contact_number = request.POST.get('contact_number')
        container_id = request.POST.get('container_id')
        package_type = request.POST.get('package_type')

        data = {
            'pseudoname': pseudoname,
            'weight': weight,
            'volumetric_measure': volumetric_measure,
            'pieces': pieces,
            'contact_number': contact_number,
            'package_type': package_type,
            'container_id': container_id
        }

        response = requests.post(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/', json=data)

        if response.status_code == 200:
            return redirect(f'/containers/{container_id}/')

        return render(request, self.template_name, {
            'error': 'Error creating package',
            'container_id': container_id,
            'containers': requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/').json()  # Re-pasar la lista de contenedores en caso de error
        })

class EditPackageView(LoginRequiredMixin, View):
    template_name = 'packages/edit_package.html'

    def get(self, request, package_id):
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}')
        package = response.json()

        response_containers = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/')
        containers = response_containers.json()

        return render(request, self.template_name, {
            'package': package,
            'containers': containers
        })

    def post(self, request, package_id):
        pseudoname = request.POST.get('pseudoname')
        weight = request.POST.get('weight')
        volumetric_measure = request.POST.get('volumetric_measure')
        pieces = request.POST.get('pieces')
        contact_number = request.POST.get('contact_number')
        container_id = request.POST.get('container_id')
        package_type = request.POST.get('package_type')

        data = {
            'pseudoname': pseudoname,
            'weight': weight,
            'volumetric_measure': volumetric_measure,
            'pieces': pieces,
            'contact_number': contact_number,
            'package_type': package_type,
            'container_id': container_id
        }

        response = requests.put(
            f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}',
            json=data)

        if response.status_code == 200:
            return redirect(f'/containers/{container_id}/')

        package = requests.get(
            f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}').json()

        # Devolver el formulario con los valores introducidos y el paquete original
        return render(request, self.template_name, {
            'error': 'Error updating package',
            'package': package,
            'containers': requests.get(
                f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/').json(),
            'data': data
        })

class PackageStatusDetailView(LoginRequiredMixin, View):
    template_name = 'packages/view_statuses.html'

    def get(self, request, package_id):
        # Obtener los estados del paquete desde el endpoint
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}')
        package = response.json()

        if response.status_code != 200:
            return render(request, self.template_name, {'error': 'Error fetching package details'})

        # Obtener los estados del paquete
        response_statuses = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/getStatusByPackage/{package_id}')
        data = response_statuses.json()

        if response_statuses.status_code != 200:
            return render(request, self.template_name, {'error': 'Error fetching statuses'})

        statuses = data.get('statuses', [])
        container_id = package.get('container_id')

        return render(request, self.template_name, {
            'statuses': statuses,
            'package_id': package_id,
            'container_id': container_id
        })

class PackageSearchView(View):
    template_name = 'packages/search.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        tracking_id = request.POST.get('tracking_id')

        # Verificar si el paquete existe
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/getInfoByTrackingId/{tracking_id}')

        if response.status_code == 200:
            # El paquete existe, redirigir a la vista de detalles del paquete
            return redirect('package_info', tracking_id=tracking_id)
        else:
            # El paquete no existe, mostrar un mensaje de error
            return render(request, self.template_name, {'error': 'El paquete con el tracking ID proporcionado no existe.'})

class PackageInfoView(View):
    template_name = 'packages/package_info.html'

    def get(self, request, tracking_id):
        # Obtener la información del paquete
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/getInfoByTrackingId/{tracking_id}')
        if response.status_code != 200:
            return render(request, self.template_name, {'error': 'Error fetching package details'})

        package_data = response.json()
        container = package_data.get('container')
        statuses = package_data.get('statuses', [])
        container_id = package_data.get('container_id')

        return render(request, self.template_name, {
            'package': package_data,
            'container': container,
            'statuses': statuses,
            'container_id': container_id,  # Pasar el ID del contenedor al contexto
        })

class DeletePackageView(LoginRequiredMixin, View):
    def post(self, request, package_id):
        # Obtener el ID del contenedor del paquete
        container_id = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}').json().get('container_id')

        # Eliminar el paquete
        delete_response = requests.delete(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}')

        if delete_response.status_code == 200:
            # Recuperar el ID del contenedor del paquete eliminado para redirigir al contenedor adecuado
            package_response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/{package_id}')

            if package_response.status_code == 404:
                # En caso de que el paquete no se encuentre, redirigir a la lista de contenedores
                return HttpResponseRedirect(reverse_lazy('container_detail', kwargs={'pk': container_id}))

            package = package_response.json()
            container_id = package.get('container_id')
            if container_id:
                # Redirigir a la vista de la lista de contenedores
                return HttpResponseRedirect(reverse_lazy('container_detail', kwargs={'pk': container_id}))

        # Redirigir a la lista de contenedores en caso de error
        return HttpResponseRedirect(reverse_lazy('container_detail', kwargs={'pk': container_id}))

class DeleteContainerView(LoginRequiredMixin, View):
    def post(self, request, pk):
        # Enviar la solicitud DELETE al endpoint de FastAPI
        response = requests.delete(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/containers/{pk}/')

        if response.status_code == 200:
            return redirect('container_list')
        else:
            return HttpResponse('Error deleting container', status=500)

class DownloadPackageReceiptView(LoginRequiredMixin, View):
    def get(self, request, package_id):
        # Realizar la solicitud al endpoint para descargar el archivo
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/downloadReceipt/{package_id}')

        if response.status_code == 200:
            # Suponiendo que el archivo se devuelve en el cuerpo de la respuesta
            file_name = response.headers.get('Content-Disposition', 'attachment; filename="default_filename"').split('filename=')[1].strip('"')
            content_type = response.headers.get('Content-Type', 'application/octet-stream')

            # Crear una respuesta con el archivo
            response_to_return = HttpResponse(response.content, content_type=content_type)
            response_to_return['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response_to_return
        else:
            return HttpResponse('Error downloading file', status=500)

class DownloadPackageLabeledView(LoginRequiredMixin, View):
    def get(self, request, package_id):
        # Realizar la solicitud al endpoint para descargar el archivo
        response = requests.get(f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/downloadLabeled/{package_id}')

        if response.status_code == 200:
            # Suponiendo que el archivo se devuelve en el cuerpo de la respuesta
            file_name = response.headers.get('Content-Disposition', 'attachment; filename="default_filename"').split('filename=')[1].strip('"')
            content_type = response.headers.get('Content-Type', 'application/octet-stream')

            # Crear una respuesta con el archivo
            response_to_return = HttpResponse(response.content, content_type=content_type)
            response_to_return['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response_to_return
        else:
            return HttpResponse('Error downloading file', status=500)

class ChangeStatusByContainerView(LoginRequiredMixin, View):
    def get(self, request, container_id):
        return render(request, 'containers/add_status_by_container.html', {'container_id': container_id})

    def post(self, request, container_id):
        status = request.POST.get('status')
        delivered = request.POST.get('delivered') == 'on'  # Verifica si el checkbox está marcado

        # Hacer la solicitud POST al endpoint FastAPI para cambiar el estado
        response = requests.post(
            f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}//containers/changeStatusByContainer/{container_id}',
            json={'status': status}
        )

        if response.status_code == 200:
            # Si el checkbox está marcado, hacer la solicitud para marcar como entregados
            if delivered:
                deliver_response = requests.put(
                    f'{os.getenv("PROTOCOL")}://{os.getenv("API_SERVER")}:{os.getenv("API_PORT")}/packages/deliverByContainer/{container_id}',
                    json={'delivered': True}  # Se puede enviar True ya que el checkbox estaba marcado
                )

                if deliver_response.status_code != 200:
                    return render(request, 'containers/add_status_by_container.html', {
                        'container_id': container_id,
                        'error': 'Error marking packages as delivered. Please try again.'
                    })

            # Mensaje de éxito
            return render(request, 'containers/add_status_by_container.html', {
                'container_id': container_id,
                'success': 'Status updated successfully.'
            })
        else:
            return render(request, 'containers/add_status_by_container.html', {
                'container_id': container_id,
                'error': 'Error updating status for all packages. Please try again.'
            })
