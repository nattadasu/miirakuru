from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# if its still in http folder, move to parent
if os.getcwd().split('\\')[-1] == 'http':
    os.chdir('..')

print(os.getcwd())

@app.route('/')
async def landing_page():
    return send_from_directory('../html', 'index.html')

@app.route('/myanimelist')
async def myanimelist_oauth():
    # response_key = request.args.get('code')
    return send_from_directory('../html', 'myanimelist.html')

@app.route('/js/<path:path>')
async def send_js(path):
    return send_from_directory('../js', path)

@app.route('/css/<path:path>')
async def send_css(path):
    return send_from_directory('../css', path)

@app.route('/assets/<path:path>')
async def send_assets(path):
    return send_from_directory('../assets', path)

def server_main():
    app.run(host='5000')

if __name__ == '__main__':
    server_main()