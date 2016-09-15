from HTMLOutput import HTMLOutput

output = HTMLOutput()

data = { "a" : 123, "b" : 456 }

output.addstring("Test Page", "This is some test content")
output.adddata("Another Test", data)

output.render()



