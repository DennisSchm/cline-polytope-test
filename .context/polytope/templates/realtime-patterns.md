# Real-time Application Patterns

## CRITICAL: Event Loop Integration for Background Threads

When building real-time applications with FastAPI, WebSockets, and background message processing (e.g., Kafka consumers), you MUST properly integrate background threads with the main async event loop.

### ❌ WRONG: Using asyncio.run() in Background Threads
<code language="python">
# This creates an isolated event loop that cannot communicate with FastAPI's main loop
def background_thread():
    for message in consumer:
        asyncio.run(websocket_manager.broadcast(message))  # WRONG!
</code>

### ✅ CORRECT: Using asyncio.run_coroutine_threadsafe()
<code language="python">
# Global reference to main event loop
main_loop = None

def background_thread():
    """Background thread that processes messages"""
    for message in consumer:
        if main_loop and not main_loop.is_closed():
            # Schedule coroutine to run in main event loop
            asyncio.run_coroutine_threadsafe(
                websocket_manager.broadcast(message), 
                main_loop
            )

def start_background_processing():
    """Initialize background thread with event loop reference"""
    global main_loop
    main_loop = asyncio.get_event_loop()
    thread = threading.Thread(target=background_thread, daemon=True)
    thread.start()
</code>

## WebSocket Connection Management

### Safe Broadcasting with Connection Cleanup
<code language="python">
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def broadcast(self, message: str):
        # Create copy to avoid modification during iteration
        connections_to_remove = []
        
        for connection in self.active_connections[:]:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.warning(f"Failed to send to WebSocket: {e}")
                connections_to_remove.append(connection)
        
        # Remove broken connections
        for connection in connections_to_remove:
            if connection in self.active_connections:
                self.active_connections.remove(connection)
</code>

### Lazy Background Service Initialization
<code language="python">
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Start background services only when first WebSocket connects
    start_background_processing()
    
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
</code>

## Message Queue Integration Patterns

### Kafka Consumer with WebSocket Broadcasting
<code language="python">
def kafka_consumer_thread():
    """Consume from Kafka and broadcast via WebSocket"""
    while True:
        try:
            consumer = KafkaConsumer(
                'topic_name',
                bootstrap_servers=['redpanda:9092'],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='latest',
                group_id='websocket_group'
            )
            
            for message in consumer:
                message_data = message.value
                # CRITICAL: Use run_coroutine_threadsafe, not asyncio.run
                if main_loop and not main_loop.is_closed():
                    asyncio.run_coroutine_threadsafe(
                        manager.broadcast(json.dumps(message_data)), 
                        main_loop
                    )
        except Exception as e:
            logger.error(f"Kafka consumer error: {e}")
            time.sleep(5)  # Retry after delay
</code>

### Resilient Message Publishing
<code language="python">
@router.post("/messages")
async def create_message(message: MessageCreate):
    # 1. Store data first (resilient pattern)
    stored_message = store_message_locally(message)
    
    # 2. Try to publish to message queue (non-blocking)
    try:
        producer = get_kafka_producer()
        if producer:
            producer.send('messages', stored_message.dict())
            producer.flush()
    except Exception as e:
        logger.error(f"Failed to publish to Kafka: {e}")
        # Don't fail the request - message is already stored
    
    return stored_message
</code>

## Common Mistakes to Avoid

1. **Never use `asyncio.run()` in background threads** - it creates isolated event loops
2. **Always use `run_coroutine_threadsafe()`** to schedule coroutines from threads
3. **Initialize background services lazily** - wait for main event loop to be available
4. **Handle broken WebSocket connections safely** - avoid modifying lists during iteration
5. **Make message publishing non-blocking** - don't fail API requests if queue is down
6. **Use proper connection cleanup** - remove dead connections to prevent memory leaks
