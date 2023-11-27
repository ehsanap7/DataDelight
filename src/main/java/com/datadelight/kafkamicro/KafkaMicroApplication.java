package com.datadelight.kafkamicro;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class KafkaMicroApplication {

    public static void main(String[] args) {
        SpringApplication.run(KafkaMicroApplication.class, args);
        System.out.println("Test");
    }

}
