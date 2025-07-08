from flask import Flask, request, jsonify, render_template
from cache_implementations import LRUCache, LFUCache

app = Flask(__name__)

# Initialize caches with capacity of 3
lru_cache = LRUCache(3)
lfu_cache = LFUCache(3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/lru/get/<key>')
def lru_get(key):
    value = lru_cache.get(key)
    return jsonify({
        'value': value,
        'state': lru_cache.get_state()
    })

@app.route('/api/lru/put', methods=['POST'])
def lru_put():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    lru_cache.put(key, value)
    return jsonify({'state': lru_cache.get_state()})

@app.route('/api/lfu/get/<key>')
def lfu_get(key):
    value = lfu_cache.get(key)
    return jsonify({
        'value': value,
        'state': lfu_cache.get_state()
    })

@app.route('/api/lfu/put', methods=['POST'])
def lfu_put():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    lfu_cache.put(key, value)
    return jsonify({'state': lfu_cache.get_state()})

if __name__ == '__main__':
    app.run(debug=True)
