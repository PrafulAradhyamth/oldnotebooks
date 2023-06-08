import cv2
import numpy as np


def stitch_images(images):
    # Create a SIFT object
    sift = cv2.SIFT_create()

    # Detect keypoints and extract descriptors for the first image
    keypoints_1, descriptors_1 = sift.detectAndCompute(images[0], None)

    # Iterate over the remaining images
    for i in range(1, len(images)):
        # Detect keypoints and extract descriptors for the current image
        keypoints_2, descriptors_2 = sift.detectAndCompute(images[i], None)

        # Create a matcher object
        matcher = cv2.BFMatcher()

        # Match the descriptors of the two images
        matches = matcher.knnMatch(descriptors_1, descriptors_2, k=2)

        # Apply ratio test to select good matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Get the keypoints from the good matches
        src_pts = np.float32([keypoints_1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints_2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Find the homography matrix
        H, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # Warp the current image to align with the first image
        warped_image = cv2.warpPerspective(images[i], H, (images[i].shape[1], images[i].shape[0]))

        # Stitch the warped image with the previous images
        stitched_image = np.concatenate((images[0], warped_image), axis=1)

        # Update the keypoints and descriptors for the next iteration
        keypoints_1, descriptors_1 = sift.detectAndCompute(stitched_image, None)

    return stitched_image


# Example usage
# Assuming you have two images img1 and img2 that you want to stitch together
img1 = cv2.imread("D:/SEM 2/DL/images/frame_0.jpg")
img2 = cv2.imread("D:/SEM 2/DL/images/frame_10.jpg")

result = stitch_images([img1, img2])

# Display the result
cv2.imshow("Stitched Image", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
