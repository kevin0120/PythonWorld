if __name__ == '__main__':
    parser = cli_parser.get_parser()

    # 自动补全命令
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    args.func(args)
