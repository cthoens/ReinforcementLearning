import unittest
import numpy as np
from CleanBotEnv import CleanBotEnv
from Models.TableModel import TableModel
from Methods.MonteCarlo import AveragingMC, AlphaMC
from Policies import EpsilonGreedyPolicy, GreedyPolicy
from utilities import MockEnv, MockPolicy

SOUTH = CleanBotEnv.BotActions.SOUTH.value
EAST = CleanBotEnv.BotActions.EAST.value
WEST = CleanBotEnv.BotActions.WEST.value
CLEAN = CleanBotEnv.BotActions.CLEAN.value


class TestAveragingMonteCarlo(unittest.TestCase):

    def test_policy_update(self):
        np.random.seed(643674)
        initial_state = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]], dtype=np.int)
        initial_obs = np.array([[2, 0, 0], [1, 0, 0], [0, 0, 0]], dtype=np.int)
        env = MockEnv(3)
        model = TableModel(env)
        greedy_policy = GreedyPolicy(model)

        policy = MockPolicy([EAST, EAST, SOUTH, WEST, WEST, CLEAN])
        mc = AveragingMC(env, model, policy)
        mc.run_episode()

        self.assertEqual(mc.metrics.first_time_visited, 6)
        self.assertEqual(mc.metrics.fifth_time_visited, 0)
        self.assertEqual(mc.metrics.episode_reward, 12)
        self.assertEqual(mc.metrics.max_action_value_delta, 0)
        self.assertEqual(greedy_policy.choose_action(initial_obs), EAST)

        mock_policy = MockPolicy([SOUTH, CLEAN])
        mc.policy = mock_policy
        mc.run_episode()

        self.assertEqual(mc.metrics.first_time_visited, 7)
        self.assertEqual(mc.metrics.fifth_time_visited, 0)
        self.assertEqual(mc.metrics.episode_reward, 16)
        self.assertEqual(mc.metrics.max_action_value_delta, 2.0)
        self.assertEqual(greedy_policy.choose_action(initial_obs), SOUTH)

    def test_smoke(self):
        np.random.seed(643674)
        env = CleanBotEnv(3)
        model = TableModel(env)
        policy = EpsilonGreedyPolicy(model, 0.1)
        mc = AveragingMC(env, model, policy)

        policy.exploration = 0.1
        episode_count = 100
        for i in range(episode_count):
            mc.run_episode()


class TestConstAlphaMonteCarlo(unittest.TestCase):

    def test_policy_update(self):
        np.random.seed(643674)
        initial_state = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]], dtype=np.int)
        initial_obs = np.array([[2, 0, 0], [1, 0, 0], [0, 0, 0]], dtype=np.int)
        env = MockEnv(3)
        model = TableModel(env)
        greedy_policy = GreedyPolicy(model)

        policy = MockPolicy([EAST, EAST, SOUTH, WEST, WEST, CLEAN])
        mc = AlphaMC(env, model, policy)
        mc.alpha = 0.005
        mc.run_episode()

        self.assertEqual(mc.metrics.episode_reward, 12)
        self.assertAlmostEqual(mc.metrics.max_action_value_delta, 0.06)
        self.assertEqual(greedy_policy.choose_action(initial_obs), EAST)

        policy = MockPolicy([EAST, EAST, SOUTH, WEST, WEST, CLEAN])
        mc = AlphaMC(env, model, policy)
        mc.run_episode()

        self.assertEqual(mc.metrics.episode_reward, 12)
        self.assertAlmostEqual(mc.metrics.max_action_value_delta, 0.05970000000670552)
        self.assertEqual(greedy_policy.choose_action(initial_obs), EAST)

        mock_policy = MockPolicy([SOUTH, CLEAN])
        mc.policy = mock_policy
        mc.run_episode()

        self.assertEqual(mc.metrics.episode_reward, 16)
        self.assertEqual(mc.metrics.max_action_value_delta, 0.08)
        self.assertEqual(greedy_policy.choose_action(initial_obs), EAST)

        mock_policy = MockPolicy([SOUTH, CLEAN])
        mc.policy = mock_policy
        mc.run_episode()

        self.assertEqual(mc.metrics.episode_reward, 16)
        self.assertEqual(mc.metrics.max_action_value_delta, 0.0796000000089407)
        self.assertEqual(greedy_policy.choose_action(initial_obs), SOUTH)


if __name__ == "__main__":
    unittest.main()
