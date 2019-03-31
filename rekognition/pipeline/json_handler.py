from rekognition.pipeline.output_handler import OutputHandler
import json

class JSONHandler(OutputHandler):
	def run(self, input_data):
		# print(input_data)

		frames = []

		for data in input_data:
			frames.append(data.get_JSON())

		filename = self.get_parent_pipeline().get_filename() + ".json"
		
		with open(filename, "w") as write_file:
			json.dump(frames, write_file)

		return input_data