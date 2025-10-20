import ollama

# List all locally available models
models = ollama.list()

# Print model names
for model in models["models"]:
    print(model)
