class Audit:
    def __init__(self, audit_id: int, auditor: str, content: str, start_time: str, publish_time: str, flagged: bool, art_id: int, chatgpt_time: str, skipped: bool, gpt_output: str, gpt_model: str):
        """Represents an audit from the database."""
        self.audit_id = audit_id
        self.auditor = auditor
        self.content = content
        self.start_time = start_time
        self.publish_time = publish_time
        self.flagged = flagged
        self.art_id = art_id
        self.chatgpt_time = chatgpt_time
        self.skipped = skipped
        self.gpt_output = gpt_output
        self.gpt_model = gpt_model

    def __str__(self) -> str:
        return f'Audit(\naudit_id={self.audit_id}, \nauditor={self.auditor}, \ncontent={self.content}, \nart_id={self.art_id}, \ngpt_output={self.gpt_output})\n'
