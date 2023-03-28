import os
from confluent_kafka import Producer
from confluent_kafka.serialization import StringSerializer, SerializationContext, MessageField
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

class KafkaProducer:  
    def __init__(self):
        self.auth = {}
        self.conf = self.read_ccloud_config("kafka/client.properties")
        self.producer = Producer(self.conf)

    def read_ccloud_config(self,config_file):
        conf = {}
        with open(config_file) as fh:
            for line in fh:
                line = line.strip()
                if len(line) != 0 and line[0] != "#" and line[:5] != 'basic': 
                    parameter, value = line.strip().split('=', 1)
                    conf[parameter] = value.strip()
                elif line[:5] == 'basic':
                    parameter, value = line.strip().split('=', 1)
                    self.auth[parameter] = value.strip()
        return conf
    
    def produce(self, topic, key, value):
        path = os.path.realpath(os.path.dirname(__file__))
        with open(f"{path}\\models\\kafkaSchema.avsc") as f:
            schema_str = f.read()


        schema_registry_conf = {'url': 'https://psrc-l6o18.us-east-2.aws.confluent.cloud',
                                'basic.auth.user.info':self.auth['basic.auth.user.info']}
        schema_registry_client = SchemaRegistryClient(schema_registry_conf)

        

        avro_serializer = AvroSerializer(schema_registry_client,
                                        schema_str,
                                        self.value_to_dict)

        self.producer.poll(0)
        self.producer.produce(topic,
                              key=key, 
                              value=avro_serializer(value, SerializationContext(topic, MessageField.VALUE)),
                              callback=self.delivery_report)
       
            
    def delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def value_to_dict(self,value, ctx):
        return dict(SampleConfidence = value.SampleConfidence,
                                Timestamp = value.Timestamp,
                                OperatingSystem = value.OperatingSystem)