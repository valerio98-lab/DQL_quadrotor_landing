import torch


class Parameters:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Parameters, cls).__new__(cls)
        return cls._instance

    def __init__(self, device="cpu"):
        self.device = device
        self.p_max = 0
        self.v_max = 0
        self.a_max = 0
        self.w_p = -100
        self.w_v = -10
        self.w_theta = -1.55
        self.w_dur = -6
        self.w_suc = 2.6
        self.w_fail = -2.6
        self.fag: float = 11.46
        self.t_max = 20
        self.r_p_max = 0
        self.r_v_max = 0
        self.r_theta_max = 0
        self.r_dur_max = 0

        self.goal_pos: torch.Tensor = torch.tensor([0.5, 0.5, 0.5])
        self.lim_pos: torch.Tensor = torch.tensor([0.5, 0.5, 0.5])
        self.goal_vel: torch.Tensor = torch.tensor([0.5, 0.5, 0.5])
        self.lim_vel: torch.Tensor = torch.tensor([0.5, 0.5, 0.5])
        self.goal_acc: torch.Tensor = torch.tensor([0.5, 0.5, 0.5])
        self.lim_acc: torch.Tensor = torch.tensor([0.5, 0.5, 0.5])
        self.r_success: float = 0
        self.r_failure: float = 0
        self.ka = 3
        self.platform_max_acc: float = 0.32
        self.gravity_magnitude: float = 9.81
        self.angle_max = self._get_angle_max()

        self.norm_goal_pos = self._normalized_state(self.goal_pos, self.p_max)
        self.norm_lim_pos = self._normalized_state(self.lim_pos, self.p_max)
        self.norm_goal_vel = self._normalized_state(self.goal_vel, self.v_max)
        self.norm_lim_vel = self._normalized_state(self.lim_vel, self.v_max)
        self.norm_goal_acc = self._normalized_state(self.goal_acc, self.a_max)
        self.norm_lim_acc = self._normalized_state(self.lim_acc, self.a_max)

    def _normalized_state(self, state: torch.Tensor, max_value):
        return torch.clip(state / max_value, -1, 1).to(self.device)

    def _get_angle_max(self):
        return (
            torch.atan((self.ka * torch.tensor(self.platform_max_acc)) / self.gravity_magnitude).to(self.device).item()
        )
