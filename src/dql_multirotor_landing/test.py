import torch
import pytest
from dql_multirotor_landing.parameters import Parameters
from dql_multirotor_landing.environment.mdp import (
    StateSpace,
    DiscreteState,
    ActionSpace,
    INCREASING,
    DECREASING,
    NOTHING,
)


@pytest.fixture
def parameters():
    """Fixture for initializing the Parameters instance."""
    return Parameters()


@pytest.fixture
def state_space():
    """Fixture for initializing the StateSpace instance."""
    return StateSpace()


@pytest.fixture
def action_space():
    """Fixture for initializing the ActionSpace instance."""
    return ActionSpace()


# ------------------------
# TESTING PARAMETERS CLASS
# ------------------------
# def test_parameters_initialization(parameters):
#     """Test whether Parameters are initialized correctly."""
#     assert parameters.p_max > 0, "p_max should be greater than 0"
#     assert parameters.v_max > 0, "v_max should be greater than 0"
#     assert parameters.a_max > 0, "a_max should be greater than 0"
#     assert parameters.angle_max is not None, "angle_max should be initialized"
#     assert parameters.w_p < 0, "w_p should be negative to reward approaching the goal"
#     assert parameters.r_success > 0, "r_success should be positive"
#     assert parameters.r_failure < 0, "r_failure should be negative"


# ------------------------
# TESTING ACTION SPACE
# ------------------------
def test_discretized_action_space(action_space):
    """Test whether action space is correctly discretized."""
    assert len(action_space.angles_set) > 0, "Angles set should not be empty"
    assert torch.all(
        action_space.angles_set <= action_space.parameters.angle_max
    ), "Angles should not exceed angle_max"


def test_get_discrete_action(action_space):
    """Test whether discrete action selection works correctly."""
    current_angle = torch.tensor(0.0)

    action_increase = action_space.get_discrete_action(current_angle, INCREASING)
    action_decrease = action_space.get_discrete_action(current_angle, DECREASING)
    action_nothing = action_space.get_discrete_action(current_angle, NOTHING)

    assert action_increase >= 0, "INCREASING should return a valid action index"
    assert action_decrease >= 0, "DECREASING should return a valid action index"
    assert action_nothing >= 0, "NOTHING should return a valid action index"


# ------------------------
# TESTING STATE SPACE
# ------------------------
def test_d_f(state_space):
    """Test whether the d_f function correctly categorizes states."""
    state = state_space.d_f(torch.tensor([0.1, 2, 0.2]), torch.randn(3), torch.randn(3))

    assert state in [0, 1, 2], "Should be in the middle category (goal)"


def test_get_discretized_state(state_space):
    """Test whether the get_discretized_state function correctly maps continuous states to discrete ones."""
    relative_pos = torch.tensor([0.3, 0.2, 0.1])
    relative_vel = torch.tensor([0.2, 0.5, 2])
    relative_acc = torch.tensor([0.1, 1, 2])

    discrete_state = state_space.get_discretized_state(relative_pos, relative_vel, relative_acc, angle_index=0)

    assert isinstance(discrete_state, DiscreteState), "Should return an instance of DiscreteState"
    assert 0 <= discrete_state.position <= 2, "Discrete position should be in range [0, 2]"
    assert 0 <= discrete_state.velocity <= 2, "Discrete velocity should be in range [0, 2]"
    assert 0 <= discrete_state.acceleration <= 2, "Discrete acceleration should be in range [0, 2]"


def test_get_reward(state_space):
    """Test whether the get_reward function correctly computes rewards."""
    current_relative_pos = torch.tensor([0.3, 0.2, 0.2])
    current_relative_vel = torch.tensor([0.3, 0.2, 0.2])
    last_relative_pos = torch.tensor([0.4, 0.3, 0.2])
    last_relative_vel = torch.tensor([0.4, 0.3, 0.2])

    reward = state_space.get_reward(current_relative_pos, current_relative_vel, last_relative_pos, last_relative_vel)

    print(reward)
    assert isinstance(reward, float), "Reward should be a float"
    assert reward < 0, "Reward should be negative when moving away from the goal"
