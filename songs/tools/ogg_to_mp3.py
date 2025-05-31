import os
import argparse
from pydub import AudioSegment

def ogg_to_mp3(input_file, output_file=None, bitrate="192k"):
    """
    把OGG文件转换成MP3文件
    :param input_file: 输入的OGG文件路径
    :param output_file: 输出的MP3文件路径，若未设置则自动生成
    :param bitrate: 输出MP3的比特率，默认是192k
    :return: 转换成功返回True，失败返回False
    """
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_file):
            print(f"错误：找不到输入文件 '{input_file}'")
            return False

        # 检查输入文件是否为OGG格式
        if not input_file.lower().endswith('.ogg'):
            print(f"错误：输入文件 '{input_file}' 不是OGG格式")
            return False

        # 如果没有指定输出文件，就自动生成
        if output_file is None:
            base_name = os.path.splitext(input_file)[0]
            output_file = f"{base_name}.mp3"

        # 检查输出目录是否存在，不存在则创建
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 加载OGG文件并进行转换
        audio = AudioSegment.from_file(input_file, format="ogg")
        audio.export(output_file, format="mp3", bitrate=bitrate)

        print(f"成功将 '{input_file}' 转换为 '{output_file}'")
        return True

    except Exception as e:
        print(f"转换过程中出错: {e}")
        return False

def batch_convert(directory, recursive=False, bitrate="192k"):
    """
    批量把目录里的OGG文件转换为MP3文件
    :param directory: 要处理的目录
    :param recursive: 是否递归处理子目录
    :param bitrate: 输出MP3的比特率，默认是192k
    :return: 成功转换的文件数量
    """
    if not os.path.isdir(directory):
        print(f"错误：目录 '{directory}' 不存在")
        return 0

    converted_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.ogg'):
                ogg_path = os.path.join(root, file)
                mp3_path = os.path.splitext(ogg_path)[0] + '.mp3'
                if ogg_to_mp3(ogg_path, mp3_path, bitrate):
                    converted_count += 1

        if not recursive:
            break

    print(f"总共成功转换了 {converted_count} 个文件")
    return converted_count

def main():
    """脚本的主入口点"""
    parser = argparse.ArgumentParser(description='OGG转MP3转换器')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='要转换的OGG文件')
    group.add_argument('-d', '--directory', help='要批量转换的目录')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理子目录')
    parser.add_argument('-b', '--bitrate', default="192k", help='输出MP3的比特率，例如128k、192k、320k等')
    parser.add_argument('-o', '--output', help='输出文件路径（仅在转换单个文件时使用）')

    args = parser.parse_args()

    if args.file:
        ogg_to_mp3(args.file, args.output, args.bitrate)
    elif args.directory:
        batch_convert(args.directory, args.recursive, args.bitrate)

if __name__ == "__main__":
    main()    