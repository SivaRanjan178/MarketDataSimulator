from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

producer = KafkaProducer(

    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.route('/send', methods=['POST'])
def producer_route():
    """
    Publish user-provided data to Kafka dynamically.
    """
    try:
        # Ensure the request is properly formatted as JSON
        if not request.is_json:
            return jsonify({"error": "Invalid Content-Type. Expected 'application/json'"}), 400

        # Parse the JSON request body
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is empty or invalid"}), 400

        # Extract and validate topic and message
        topic = data.get('topic', 'market_data')  # Default topic
        message = data.get('message')

        if not isinstance(message, dict) or not message:
            return jsonify({"error": "Invalid or missing 'message' field, must be a non-empty dictionary"}), 400

        # Publish the message to Kafka
        producer.send(topic, value=message)
        producer.flush()

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    return jsonify({"status": "success", "topic": topic,  "message": message}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5002)
