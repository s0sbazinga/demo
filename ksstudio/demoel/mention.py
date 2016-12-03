class Mention:
    def __init__(self, span=(), mtype='', mesh_id='', wid=-1, chebi_id=-1):
        self.span = span
        self.mtype = mtype
        self.mesh_id = mesh_id
        self.wid = wid
        self.chebi_id = chebi_id

    @staticmethod
    def mention_conflict(cur_mention, mention_list):
        for mention in mention_list:
            if not (cur_mention.span[1] < mention.span[0] or cur_mention.span[0] > mention.span[1]):
                return True
        return False

    @staticmethod
    def merge_mention_list(new_list, dst_list):
        for mention in new_list:
            if not Mention.mention_conflict(mention, dst_list):
                dst_list.append(mention)
