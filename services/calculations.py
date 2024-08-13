import cv2 as cv
import numpy as np
import os

def calculate_offset(image_1, image_2, good_threshold=0.7):
    sift = cv.SIFT_create()
    key_points_1, descriptors_1 = sift.detectAndCompute(image_1, None)
    key_points_2, descriptors_2 = sift.detectAndCompute(image_2, None)
    
    if descriptors_1 is None or descriptors_2 is None:
        return float('inf')  # No features could be detected.

    flann_index_kdtree = 1
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)
    good_matches = [m for m, n in matches if m.distance < good_threshold * n.distance]
    
    if not good_matches:
        return float('inf')

    src_pts = np.float32([key_points_1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([key_points_2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    
    transformation, _ = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    if transformation is None:
        return float('inf')

    h, w = image_1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    destination = cv.perspectiveTransform(pts, transformation)
    
    # Calculate Euclidean distance from the origin to the transformed position
    offset = np.linalg.norm(destination[0][0] - np.array([0, 0]))
    return offset

def analyze_image_stack(folder_path):
    image_files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.png')])
    images = [cv.imread(path, cv.IMREAD_GRAYSCALE) for path in image_files]

    if any(img is None for img in images):
        print("Some images failed to load; check file paths and formats.")
        return None
    
    offsets = []
    for i in range(len(images) - 1):
        offset = calculate_offset(images[i], images[i + 1])
        if offset != float('inf'):
            offsets.append(offset)

    if not offsets:
        print("No valid offsets were computed.")
        return None

    average_offset = np.mean(offsets)
    max_offset = max(offsets)
    field_of_view = images[0].shape[0] if images else 0
    max_percentage_fov = (max_offset / field_of_view) * 100 if field_of_view else 0

    return {
        "average_offset": average_offset,
        "max_offset": max_offset,
        "max_percentage_fov": max_percentage_fov,
        "number_of_offsets": len(offsets)
    }

# Specify the path to the folder containing your images
folder_path = r'C:\Users\admin\Desktop\Images-1'
results = analyze_image_stack(folder_path)
print("Results:", results)