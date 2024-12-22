from .root.rootRoute import bp_root
from .upload.uploadRoute import bp_upload
from .translate.translateRoute import bp_translate

all_blueprints = [bp_root, bp_upload, bp_translate]
