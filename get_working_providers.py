from g4f.active_providers import get_active_model_providers

working_providers = get_active_model_providers()

print("\nWorking providers by model:")
for model, providers in working_providers.items():
    print(f"{model}: {', '.join(providers)}")
