package com.datadelight.kafkamicro;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.KStream;

import java.util.Properties;

public class DataProcessingStreamApp {

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "cdc-data-processing-app");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass().getName());

        StreamsBuilder builder = new StreamsBuilder();

        String sourceTopic = "raw-cdc-data";
        String destinationTopic = "processed-cdc-data";

        KStream<String, String> cdcStream = builder.stream(sourceTopic);

        KStream<String, String> processedStream = cdcStream
                .mapValues(DataProcessingStreamApp::handleMissingValues)
                .mapValues(DataProcessingStreamApp::applyFeatureEngineering);

        processedStream.to(destinationTopic);

        KafkaStreams streams = new KafkaStreams(builder.build(), props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }

    private static String handleMissingValues(String value) {
        if (value != null) {
            return value;
        } else return null;
    }

    private static String applyFeatureEngineering(String value) {
        if (value != null) {
            return value;
        } else {
            return null;
        }
    }
}

