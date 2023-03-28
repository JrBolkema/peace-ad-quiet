from kafka.kafkaPublisher import KafkaProducer

class Producer:
    def __init__(self):
        self.producer = KafkaProducer()
        self.muteTopic = "peace-ad-quiet.mute.logs"
        self.unmuteTopic = "peace-ad-quiet.unmute.logs"

    def produceMuteLog(self,key,value):
        self.producer.produce(self.muteTopic,key,value)

    def produceUnmuteLog(self,key,value):
        self.producer.produce(self.unmuteTopic,key,value)