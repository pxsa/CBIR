from django.shortcuts import render
from django.http import HttpResponse
from .forms import ImageUploadForm
from .process import image_process, image_feedback_process
import os
from django.conf import settings
from .models import UploadedImage
from .vgg import VGGModel
from django.http import JsonResponse
import time


# Create your views here.
def something(request):
	return render(request, 'home.html', context={'name':"Hii"})


def upload_image(request):
	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			uploaded_image = form.save()
			# process !!!
			result = image_process(uploaded_image.image)
			return render(request, 'home.html', context={
					'uploaded_image': uploaded_image.image,
					'matched_images': result,
				})

	else:
		form = ImageUploadForm()
		
	return render(request, 'home.html', {'form': form})		


def feedback(request):
	if request.method == 'POST':
		raw_selected_images_path = request.POST.getlist('relevant_images')
		selected_images_path = [os.path.join(settings.MEDIA_ROOT, path) for path in raw_selected_images_path]
		original_image_path = os.path.join(settings.MEDIA_ROOT, request.POST['original_image'])
		result = image_feedback_process(selected_images_path, original_image_path)
		print('\n',result, '\n')		
		return render(request, 'home.html', context={
			'uploaded_image': request.POST['original_image'],
			'matched_images': result,
		})

	else:
		return render(request, 'test_feedback.html')
	

def arrange_model(request):
	# vgg = VGGModel()
	# vgg.extract_all_features()
	# vgg.make_h5f_file()

	return render(request, 'vision/arrange_model.html')


def start_process(request):
    # Simulate a long-running process
    for i in range(1, 101):
        request.session['progress'] = i  # Store progress in session
        time.sleep(1)  # Simulate time-consuming task
    
    return JsonResponse({'message': 'Process completed!'})


def get_progress(request):
    progress = request.session.get('progress', 0)
    return JsonResponse({'progress': progress})