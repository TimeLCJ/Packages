class SavePath:
    """
    Why is this a class?
    Why do I have a class for creating and parsing save paths?
    What am I doing with my life?
    """

    def __init__(self, model_name: str, epoch: int, iteration: int):
        self.model_name = model_name
        self.epoch = epoch
        self.iteration = iteration

    def get_path(self, root: str = ''):
        file_name = self.model_name + '_' + str(self.epoch) + '_' + str(self.iteration) + '.pth'
        return os.path.join(root, file_name)

    @staticmethod
    def from_str(path: str):
        file_name = os.path.basename(path)

        if file_name.endswith('.pth'):
            file_name = file_name[:-4]

        params = file_name.split('_')

        if file_name.endswith('interrupt'):
            params = params[:-1]

        model_name = '_'.join(params[:-2])
        epoch = params[-2]
        iteration = params[-1]

        return SavePath(model_name, int(epoch), int(iteration))

    @staticmethod
    def remove_interrupt(save_folder):
        for p in Path(save_folder).glob('*_interrupt.pth'):
            p.unlink()

    @staticmethod
    def get_interrupt(save_folder):
        for p in Path(save_folder).glob('*_interrupt.pth'):
            return str(p)
        return None

    @staticmethod
    def get_latest(save_folder, config):
        """ Note: config should be config.name. """
        max_iter = -1
        max_name = None

        for p in Path(save_folder).glob(config + '_*'):
            path_name = str(p)

            try:
                save = SavePath.from_str(path_name)
            except:
                continue

            if save.model_name == config and save.iteration > max_iter:
                max_iter = save.iteration
                max_name = path_name

        return max_name