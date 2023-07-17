from g4f import Provider


class Model:
    class model:
        name: str
        base_provider: str
        best_provider: str

    class gpt_35_turbo:
        name: str = 'gpt-3.5-turbo'
        base_provider: str = 'openai'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_35_turbo_poe:
        name: str = 'gpt-3.5-turbo-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_35_turbo_16k:
        name: str = 'gpt-3.5-turbo-16k'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_35_turbo_16k_poe:
        name: str = 'gpt-3.5-turbo-16k-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_4:
        name: str = 'gpt-4'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_4_0613:
        name: str = 'gpt-4-0613'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_4_poe:
        name: str = 'gpt-4-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_4_32k:
        name: str = 'gpt-4-32k'
        base_provider: str = 'reversed'
        best_provider: Provider.Provider = Provider.Chimera

    class gpt_4_32k_poe:
        name: str = 'gpt-4-32k-poe'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Chimera

    class claude_instant_100k:
        name: str = 'claude-instant-100k'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Chimera

    class claude_instant:
        name: str = 'claude-instant'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Chimera

    class claude_2_100k:
        name: str = 'claude-2-100k'
        base_provider: str = 'anthropic'
        best_provider: Provider.Provider = Provider.Chimera

    class sage:
        name: str = 'sage'
        base_provider: str = 'poe'
        best_provider: Provider.Provider = Provider.Chimera


class ModelUtils:
    convert: dict = {
        'gpt-3.5-turbo': Model.gpt_35_turbo,
        'gpt-3.5-turbo-poe': Model.gpt_35_turbo_poe,
        'gpt-3.5-turbo-16k': Model.gpt_35_turbo_16k,
        'gpt-3.5-turbo-16k-poe': Model.gpt_35_turbo_16k_poe,
        'gpt-4': Model.gpt_4,
        'gpt-4-0613': Model.gpt_4_0613,
        'gpt-4-poe': Model.gpt_4_poe,
        'gpt-4-32k': Model.gpt_4_32k,
        'gpt-4-32k-poe': Model.gpt_4_32k_poe,

        'claude-instant-100k': Model.claude_instant_100k,
        'claude-instant': Model.claude_instant,
        'claude-2-100k': Model.claude_2_100k,

        'sage': Model.sage,
    }
