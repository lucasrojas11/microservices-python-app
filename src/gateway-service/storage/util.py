import pika, json

def upload (f, fs, channel, access):
    try: 
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "internal server error, fs level", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.BasicProperties.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as err:
        print(err)
        fs.delete(fid)
        return f"internal server error, rabbitmq issue, {err}", 500