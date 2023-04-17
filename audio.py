class Audio:
    def __init__(self, id: int, created_at: str, entity_type: str, entity_id: int, link: str):
        self.id = id
        self.created_at = created_at
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.link = link

    def __str__(self):
        return f"Audio(id={self.id}, created_at={self.created_at}, entity_type={self.entity_type}, entity_id={self.entity_id}, link={self.link})"
