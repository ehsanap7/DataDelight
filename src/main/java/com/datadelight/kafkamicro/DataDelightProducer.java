package com.datadelight.kafkamicro;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.Producer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Properties;

public class DataDelightProducer {
    public static void main(String[] args) {
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");

        try (Producer<String, String> producer = new KafkaProducer<>(props)) {
            String[] symbols = {"USDCAD", "USDCAD", "USDCHF", "apple", "EURUSD"};

            for (String symbol : symbols) {
                String data = getDataForSymbol(symbol);

                producer.send(new ProducerRecord<>("MarketData", symbol, data));
            }
        }
    }

    private static String getDataForSymbol(String symbol) {
        return "mock_data_for_" + symbol;
    }
}
