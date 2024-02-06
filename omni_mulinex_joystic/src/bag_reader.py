"""script that reads ROS2 messages from an MCAP bag using the rosbag2_py API."""
import argparse
import scipy.io

import rosbag2_py
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message


def read_messages(input_bag: str):
    reader = rosbag2_py.SequentialReader()
    reader.open(
        rosbag2_py.StorageOptions(uri=input_bag, storage_id="mcap"),
        rosbag2_py.ConverterOptions(
            input_serialization_format="cdr", output_serialization_format="cdr"
        ),
    )

    topic_types = reader.get_all_topics_and_types()

    def typename(topic_name):
        for topic_type in topic_types:
            if topic_type.name == topic_name:
                return topic_type.type
        raise ValueError(f"topic {topic_name} not in bag")

    while reader.has_next():
        topic, data, timestamp = reader.read_next()
        msg_type = get_message(typename(topic))
        msg = deserialize_message(data, msg_type)
        yield topic, msg, timestamp
    del reader


def main():
    joints_position = [[]]
    joints_velocity = [[]]
    joints_torque = [[]]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input", help="input bag path (folder or filepath) to read from"
    )

    args = parser.parse_args()
    for topic, msg, timestamp in read_messages(args.input):
        if topic == "state_broadcaster/joints_state":
            joints_position += [msg.position]
            joints_velocity += [msg.velocity]
            joints_torque += msg.effort
            print(f"{topic} ({type(msg).__name__}) [{timestamp/1e9}]: '{msg.name}'")

        # if topic == "Joystic_Command":

        # print(f"{topic} ({type(msg).__name__}) [{timestamp}]: '{msg}'")
    #     pippo = msg
    # name_file = "/home/pietro/Desktop/bags"
    # scipy.io.savemat(name_file, mdict={'data': pippo})


if __name__ == "__main__":
    main()
