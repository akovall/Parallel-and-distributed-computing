import time, threading, random
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError

def process_message(message):
    # Імітація обробки повідомлення, яка може викликати помилку
    if random.random() < 0.1:
        raise ValueError("Виняткова ситуація під час обробки даних")
    time.sleep(random.uniform(0.01, 0.05))
    print(f"Потік {threading.current_thread().name}: Обробив повідомлення з offset={message.offset}")

def consume_task(task_id):
    consumer = None
    try:
        consumer = KafkaConsumer(
            "inbox", 
            bootstrap_servers="kafka:9092", 
            group_id=f"svc-{task_id}", 
            enable_auto_commit=True,
            auto_offset_reset="earliest"
        )
        partitions = list(consumer.partitions_for_topic("inbox"))
        if len(partitions) > 0:
            consumer.assign([TopicPartition("inbox", partitions[0])])

        for message in consumer:
            try:
                process_message(message)
                if random.random() < 0.05:
                    print(f"Потік {threading.current_thread().name}: Скидаю позицію, щоб перезапустити...")
                    consumer.seek(message.partition, 0)
                    
            except Exception as e:
                print(f"Потік {threading.current_thread().name}: Помилка обробки: {e}")
                pass
                
    except KafkaError as e:
        print(f"Потік {threading.current_thread().name}: Помилка Kafka: {e}")
    finally:
        if consumer:
            consumer.close()

# Створюємо кілька потоків, які будуть конкурувати
threads = [threading.Thread(target=consume_task, args=(i,), name=f"Consumer-{i}") for i in range(3)]
[t.start() for t in threads]
[t.join() for t in threads]
