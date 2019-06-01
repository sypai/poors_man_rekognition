from .output_handler import OutputHandler
from ...utils import visualization_utils_color as vis_util
from progress.bar import Bar
import av, os
from PIL import Image

class VideoOutputHandler(OutputHandler):
	def run(self, data):

		if not os.path.exists("output"):
			os.mkdir("output")

		container = av.open("output/" + self.output_name + '_output.mp4', mode='w')
		stream = None

		fps = 25

		frames_reader = data.frames_reader

		print("Saving processed video")
		bar = Bar('Processing', max = frames_reader.frames_num)

		frames_generator = frames_reader.get_frames(1)

		i = 0

		for frames_data, frames_pts in frames_generator:
			image = frames_data

			if stream is None:
				[h, w] = image.shape[:2]
				print(h, w)
				stream = container.add_stream('h264', rate=fps)
				stream.height = h
				stream.width = w

			frame_boxes = data._frames_face_boxes[i]

			if len(frame_boxes):
				for f in range(len(frame_boxes)):
					ymin, xmin, ymax, xmax = frame_boxes[f]
					name = data._frames_face_names[i][f][0]

					vis_util.draw_bounding_box_on_image_array(image,
													 ymin,
													 xmin,
													 ymax,
													 xmax,
													 display_str_list=[name])

			frame = av.VideoFrame.from_ndarray(image, format='rgb24')
			for packet in stream.encode(frame):
				container.mux(packet)

			i += 1
			bar.next()

		# flush stream
		for packet in stream.encode():
			container.mux(packet)
		
		container.close()
		bar.finish()