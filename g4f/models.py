from g4f import Provider


class Model:
    class model:
        name: str
        base_provider: str
        best_provider: str

    class gpt_35_turbo:
        name: str = 'gpt-3.5-turbo'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_35_turbo_0301:
        name: str = 'gpt-3.5-turbo-0301'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_35_turbo_poe:
        name: str = 'gpt-3.5-turbo-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_35_turbo_16k:
        name: str = 'gpt-3.5-turbo-16k'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_35_turbo_16k_poe:
        name: str = 'gpt-3.5-turbo-16k-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_4:
        name: str = 'gpt-4'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_4_0314:
        name: str = 'gpt-4-0314'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_4_poe:
        name: str = 'gpt-4-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_4_32k:
        name: str = 'gpt-4-32k'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Naga

    class gpt_4_32k_poe:
        name: str = 'gpt-4-32k-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Naga

    class claude_instant_100k:
        name: str = 'claude-instant-100k'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Naga

    class claude_instant:
        name: str = 'claude-instant'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Naga

    class claude_2:
        name: str = 'claude-2'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Naga

    class claude_2_100k:
        name: str = 'claude-2-100k'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Naga

    class llama_2_7b_chat:
        name: str = 'llama-2-7b-chat'
        base_provider: str = 'llama'
        best_provider: Provider.Provider = Provider.Naga

    class llama_2_13b_chat:
        name: str = 'llama-2-13b-chat'
        base_provider: str = 'llama'
        best_provider: Provider.Provider = Provider.Naga

    class llama_2_70b_chat:
        name: str = 'llama-2-70b-chat'
        base_provider: str = 'llama'
        best_provider: Provider.Provider = Provider.Naga
    
    class oasst_sft_6_llama_30b:
        name: str = 'oasst-sft-6-llama-30b'
        base_provider: str = 'huggingface-chat'
        best_provider: Provider.Provider = Provider.Naga

    class falcon_180b_chat:
        name: str = 'falcon-180b-chat'
        base_provider: str = 'huggingface-chat'
        best_provider: Provider.Provider = Provider.Naga



class ModelUtils:
    convert: dict = {
        'gpt-3.5-turbo': Model.gpt_35_turbo,
        'gpt-3.5-turbo-0301': Model.gpt_35_turbo_0301,
        'gpt-3.5-turbo-poe': Model.gpt_35_turbo_poe,
        'gpt-3.5-turbo-16k': Model.gpt_35_turbo_16k,
        'gpt-3.5-turbo-16k-poe': Model.gpt_35_turbo_16k_poe,
        'gpt-4': Model.gpt_4,
        'gpt-4-0314': Model.gpt_4_0314,
        'gpt-4-poe': Model.gpt_4_poe,
        'gpt-4-32k': Model.gpt_4_32k,
        'gpt-4-32k-poe': Model.gpt_4_32k_poe,

        'claude-instant-100k': Model.claude_instant_100k,
        'claude-instant': Model.claude_instant,
        'claude-2': Model.claude_2,
        'claude-2-100k': Model.claude_2_100k,

        'oasst-sft-6-llama-30b': Model.oasst_sft_6_llama_30b,
        'llama-2-7b-chat': Model.llama_2_7b_chat,
        'llama-2-13b-chat': Model.llama_2_13b_chat,
        'llama-2-70b-chat': Model.llama_2_70b_chat,
        'falcon-180b-chat': Model.falcon_180b_chat
    }
