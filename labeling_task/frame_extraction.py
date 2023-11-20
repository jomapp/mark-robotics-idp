import imageio.v3 as iio

VIDEO_PATH = "sample_video.mp4"

for idx, frame in enumerate(iio.imiter(VIDEO_PATH)):
    iio.imwrite(f"extracted_images/frame{idx:03d}.jpg", frame)