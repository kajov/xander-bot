FROM ubuntu:18.04

RUN sudo apt update
RUN sudo apt install python3.8

CMD [pip install -r requirements.txt]
CMD [python Feedback.py]
