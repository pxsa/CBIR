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

			# PROCESS !!!

			# Custom Model
			# matched_images = image_process(uploaded_image.image)

			# VGG Model
			vgg = VGGModel()
			matched_images, scores = vgg.image_process(uploaded_image.image)

			return render(request, 'home.html', context={
					'uploaded_image': uploaded_image.image,
					'matched_images': matched_images,
					'scores': scores,
				})
	else:
		form = ImageUploadForm()
		
	return render(request, 'home.html', {'form': form})		


def feedback(request):
	if request.method == 'POST':
		raw_selected_images_path = request.POST.getlist('relevant_images')
		selected_images_path = [os.path.join(settings.STATICFILES_DIRS[0], path) for path in raw_selected_images_path]
		original_image_path = os.path.join(settings.MEDIA_ROOT, request.POST['original_image'])
		
		# PROCESS !!!

		# Custom Model
		# updated_images = image_feedback_process(selected_images_path, original_image_path)

		# VGG Model
		vgg = VGGModel()
		updated_images, scores = vgg.image_feedback_process(selected_images_path, original_image_path)
		# print(selected_images_path)
		# print('\n',updated_images, '\n')		
		
		return render(request, 'home.html', context={
			'uploaded_image': request.POST['original_image'],
			'matched_images': updated_images,
			'scores': scores,
		})

	else:
		return render(request, 'home.html')
	

def arrange_model(request):
	return render(request, 'vision/arrange_model.html')





def start_process(request):
    # # Simulate a long-running process
    # for i in range(1, 101):
    #     request.session['progress'] = i  # Store progress in session
    #     time.sleep(1)  # Simulate time-consuming task
    # return JsonResponse({'message': 'Process completed!'})
	
	vgg = VGGModel()
	vgg.extract_all_features()
	vgg.make_h5f_file()
	return render(request, 'vision/arrange_model.html', context={'status':'Process completed!'})
    

def get_progress(request):
    progress = request.session.get('progress', 0)
    return JsonResponse({'progress': progress})
