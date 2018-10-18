from config import configs
from onelove import create_app

config = configs['development']
app = create_app(config)
