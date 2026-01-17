import time, threading, random
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import KafkaError


# DLQ для "поганих" повідомлень
dead_letter_queue = []


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
            group_id="svc",                   #спільна група для всіх
            enable_auto_commit=False,         #автокоміт вимкнено
            auto_offset_reset="earliest"
        )
        partitions = list(consumer.partitions_for_topic("inbox"))
        if len(partitions) > 0:
            consumer.assign([TopicPartition("inbox", partitions[0])])

        for message in consumer:
            try:
                process_message(message)
                consumer.commit()  #явний commit після обробки, також видалено випадковий seek

            except Exception as e:
                #DLQ для "поганих" повідомлень
                print(f"Потік {threading.current_thread().name}: Помилка обробки: {e}")
                dead_letter_queue.append((message, str(e)))
                consumer.commit()  

    except KafkaError as e:
        print(f"Потік {threading.current_thread().name}: Помилка Kafka: {e}")
    finally:
        if consumer:
            consumer.close()


# Створюємо кілька потоків, які будуть конкурувати
threads = [threading.Thread(target=consume_task, args=(i,), name=f"Consumer-{i}") for i in range(3)]
[t.start() for t in threads]
[t.join() for t in threads]
