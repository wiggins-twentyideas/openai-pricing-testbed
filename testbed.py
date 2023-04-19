import openai
import pprint
import sys
import json


from prompt_toolkit import prompt


openai.api_key = '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'

_initial_usage = {
    "completion_tokens": 0,
    "prompt_tokens": 0,
    "total_tokens": 0
}

class TestBedApp:
	cmd_characters = "/\\"
	messages = []
	responses = []
	openai_model = "gpt-3.5-turbo"
	running = True
	usage = _initial_usage
	debug = False
	token_price = 0.002/1000.0 # $0.002 per 1,000 tokens

	def main(self, args):
		self.cmd_help("help","")
		while self.running:
			self.repl()

	def usage_cost(self):
		return self.usage["total_tokens"] * self.token_price

	def prompt_string(self):
		return "\n\n(${:0.6f}) (messages:{msg}) (completion_tokens:{cmpl}) (prompt_tokens:{prompt}) (total_tokens:{total})\n?> ".format(
			self.usage_cost(),
			msg=len(self.messages),
			cmpl=self.usage['completion_tokens'],
			prompt=self.usage['prompt_tokens'],
			total=self.usage['total_tokens'],
		)

	def repl(self):
		try:
			user_input = prompt(self.prompt_string())
		except EOFError as e:
			return self.quit()

		if user_input[0] in self.cmd_characters:
			try:
				cmd, params = user_input[1:].split(" ", 1)
			except ValueError as e:
				cmd, params = user_input[1:], ""

			method = getattr(self, "cmd_{}".format(cmd.lower()), None)
			if callable(method):
				method(cmd, params)
			else:
				print("Unknown command: {}".format(cmd))

		else:
			self.append_user_content(user_input)


	def append_user_content(self, content):
		self.messages.append({
			"role": "user",
			"content": content
		})
		self.send_chats()

	def send_chats(self):
		response = openai.ChatCompletion.create(
			model = self.openai_model,
			messages = self.messages
		)
		self.handle_response(response)

	def handle_response(self, response):
		if self.debug:
			pprint.pprint(response)

		self.responses.append({
			"messages": self.messages,
			"responses": response
		})

		# import pdb; pdb.set_trace()
		self.usage['completion_tokens'] += response.usage.completion_tokens
		self.usage['prompt_tokens'] += response.usage.prompt_tokens
		self.usage['total_tokens'] += response.usage.total_tokens

		choice = response.choices[0]
		print("{}\n".format(choice.message.content))
		self.messages.append(choice.message)

	def quit(self):
		self.running = False

	def cmd_quit(self, cmd, args):
		print("exiting.")
		self.quit()

	def cmd_reset(self, cmd, args):
		self.usage = _initial_usage
		self.messages = []

	def cmd_system(self, cmd, content):
		self.messages.append({
			"role": "system",
			"content": content
		})

	def cmd_messages(self, cmd, args):
		pprint.pprint(self.messages)

	def cmd_responses(self, cmd, args):
		pprint.pprint(self.responses)

	def cmd_save(self, cmd, args):
		filename = args.strip()
		if len(filename) < 1:
			print("Usage: /save <filename>")
			return

		with open(filename, 'w') as fh:
			fh.write(json.dumps({
				"total_cost": self.usage_cost(),
				"messages": self.messages,
				"responses": self.responses,
				"usage": self.usage,
			}))
		print("Session saved to {}".format(filename))

	def cmd_help(self, cmd, args):
		print(
			f"/quit\n"
			f"/reset - resets session and usage counters\n"
			f"/system <message> - appends a system message\n"
			f"/messages - prints session messages\n"
			f"/responses - prints session responses\n"
			f"/save <filename.json> - dump session to json file\n"
			f"/help\n"
		)


	

if __name__ == '__main__':
	app = TestBedApp()
	app.main(sys.argv)
