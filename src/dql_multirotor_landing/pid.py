from typing import Any

import torch
import torch.nn.functional as F


class PIDController:
    """Pid controller that controls `height` and `yaw`"""

    def __init__(
        self,
        kp: Any = [4.5, 2],
        ki: Any = [4, 3],
        kd: Any = [6.5, 5],
        set_point: Any = [0, 0],
        device="cpu",
        *,
        windup_max=10,
        sample_time=0.02,
    ):
        self.device = device
        self.kp = torch.tensor(kp).to(self.device)
        self.ki = torch.tensor(ki).to(self.device)
        self.kd = torch.tensor(kd).to(self.device)
        self.set_point = torch.tensor(set_point).to(self.device)
        self.windup_max = torch.tensor(windup_max).to(self.device)

        self.p_term = torch.zeros_like(self.kp).to(self.device).float()
        self.i_term = torch.zeros_like(self.ki).to(self.device).float()
        self.d_term = torch.zeros_like(self.kd).to(self.device).float()

        self.sample_time = sample_time
        self.last_error = torch.zeros_like(self.kp).to(self.device)
        self.last_y = torch.zeros_like(self.kp).to(self.device)

    def output(self, y_measured):
        y_measured = torch.tensor(y_measured).to(self.device)
        # Compute the current error
        error = self.set_point - y_measured

        # Get the PID values
        self.p_term = self.kp * error
        self.d_term = self.kd * (self.last_y - y_measured) / self.sample_time
        self.i_term += self.ki * error * self.sample_time
        print("I_term: ", self.i_term)

        # TODO: Understand if it's needed.
        # Anti-windup
        # self.i_term = torch.clamp(self.i_term, -self.windup_max, self.windup_max)

        # Salvataggio stati
        self.last_error = error
        self.last_y = y_measured
        result = self.p_term + self.i_term + self.d_term
        # print(f"Result: {result}, I_term: {self.i_term}")
        limits = torch.tensor([[-200, 10], [-1, 1]])
        result = torch.where(result < 0, torch.clamp_min(result, limits[:, 0]), torch.clamp_max(result, limits[:, 1]))
        return result

    def reset(self):
        self.p_term = torch.zeros_like(self.kp).to(self.device).float()
        self.i_term = torch.zeros_like(self.ki).to(self.device).float()
        self.d_term = torch.zeros_like(self.kd).to(self.device).float()
        self.last_error = torch.zeros_like(self.kp).to(self.device)
        self.last_y = torch.zeros_like(self.kp).to(self.device)


a, b = PIDController().output(([10, 10]))
print(a.item(), b.item())
