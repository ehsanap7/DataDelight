package org.example;

import com.yahoofinance.Stock;
import com.yahoofinance.YahooFinance;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.io.IOException;
import java.util.Properties;

public class Producer2 {
    public static void main(String[] args) throws IOException {
        // Configure Kafka producer
        Properties properties = new Properties();
        properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");
        properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer");

        Producer<String, String> producer = new KafkaProducer<>(properties);

        // Fetch data from Yahoo Finance API for GBPUSD=X
        Stock stock = YahooFinance.get("GBPUSD=X");

        // Prepare the message to send to Kafka
        String key = "GBPUSD=X";
        String value = String.format("Price: %s, Change: %s", stock.getQuote().getPrice(), stock.getQuote().getChange());

        // Produce the message to a Kafka topic
        ProducerRecord<String, String> record = new ProducerRecord<>("stock-prices", key, value);
        producer.send(record, (metadata, exception) -> {
            if (exception != null) {
                // Handle exception
                exception.printStackTrace();
            } else {
                System.out.printf("Produced record to topic %s partition %s with offset %s%n", metadata.topic(), metadata.partition(), metadata.offset());
            }
        });

        // Close the producer
        producer.close();
    }
}

