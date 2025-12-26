using Xunit;

namespace EverySecondTurnSolver.Tests;

public class EverySecondTurnSolverTest
{
    private const char X = EverySecondTurnSolver.Circle;
    private const char _ = EverySecondTurnSolver.Empty;

    [Fact]
    public void TestSolution_6_6_37g81()
    {
        // https://gridpuzzle.com/every-second-turn/37g81
        var gridData = new char[,]
        {
            { _, _, _, _, _, X },
            { _, X, _, _, _, _ },
            { _, _, _, _, X, _ },
            { X, _, _, X, _, _ },
            { _, _, X, _, _, X },
            { X, _, _, _, _, _ },
        };

        const string expectedSolutionStr =
            " ┌──────────────┐ \n" +
            " │  ┌────────┐  │ \n" +
            " │  │  ┌─────┘  │ \n" +
            " └──┘  │  ┌─────┘ \n" +
            " ┌─────┘  └─────┐ \n" +
            " └──────────────┘ ";

        var solver = new EverySecondTurnSolver(gridData);
        var solution = solver.GetSolution();
        Assert.NotNull(solution);
        Assert.Equal(expectedSolutionStr, solution.ToString());

        var otherSolution = solver.GetOtherSolution();
        Assert.True(otherSolution == null || otherSolution.Rows == 0);
    }

    [Fact]
    public void TestSolution_6_6_3e9k2()
    {
        // https://gridpuzzle.com/every-second-turn/3e9k2
        var gridData = new char[,]
        {
            { X, _, _, _, _, _ },
            { _, _, _, _, _, X },
            { _, _, X, _, _, _ },
            { _, _, _, _, X, _ },
            { _, X, _, _, _, _ },
            { _, _, _, _, _, X }
        };

        const string expectedSolutionStr =
            " ┌──────────────┐ \n" +
            " │  ┌───────────┘ \n" +
            " │  │  ┌────────┐ \n" +
            " │  │  └─────┐  │ \n" +
            " │  └────────┘  │ \n" +
            " └──────────────┘ ";

        var solver = new EverySecondTurnSolver(gridData);
        var solution = solver.GetSolution();
        Assert.NotNull(solution);
        Assert.Equal(expectedSolutionStr, solution.ToString());

        var otherSolution = solver.GetOtherSolution();
        Assert.True(otherSolution == null || otherSolution.Rows == 0);
    }

    [Fact]
    public void TestSolution_10_10_0ygm8()
    {
        // https://gridpuzzle.com/every-second-turn/0ygm8
        var gridData = new[,]
        {
            { X, _, _, _, _, X, _, _, X, _ },
            { _, _, _, X, _, _, _, X, _, _ },
            { _, _, X, _, _, _, X, _, _, _ },
            { _, X, _, _, X, _, _, _, X, _ },
            { X, _, _, _, X, _, _, _, _, _ },
            { _, _, _, _, _, _, _, _, X, _ },
            { _, X, _, X, _, _, X, _, _, _ },
            { _, _, _, X, _, X, _, X, _, X },
            { _, X, _, _, X, _, _, _, X, _ },
            { _, _, X, _, _, _, _, _, _, X }
        };

        const string expectedSolutionStr =
            " ┌───────────┐  ┌─────┐  ┌──┐ \n" +
            " │  ┌─────┐  │  │  ┌──┘  │  │ \n" +
            " │  │  ┌──┘  │  │  └─────┘  │ \n" +
            " └──┘  │  ┌──┘  └────────┐  │ \n" +
            " ┌──┐  │  │  ┌───────────┘  │ \n" +
            " │  │  │  │  └───────────┐  │ \n" +
            " │  └──┘  └─────┐  ┌─────┘  │ \n" +
            " │  ┌─────┐  ┌──┘  └──┐  ┌──┘ \n" +
            " │  └──┐  │  └────────┘  └──┐ \n" +
            " └─────┘  └─────────────────┘ ";

        var solver = new EverySecondTurnSolver(gridData);
        var solution = solver.GetSolution();
        Assert.NotNull(solution);
        Assert.Equal(expectedSolutionStr, solution.ToString());

        var otherSolution = solver.GetOtherSolution();
        Assert.True(otherSolution == null || otherSolution.Rows == 0);
    }

    [Fact]
    public void TestSolution_16_16_0zny2()
    {
        // https://gridpuzzle.com/every-second-turn/0zny2
        var gridData = new[,]
        {
            { X, _, X, _, X, _, X, _, _, _, _, _, _, _, X, _ },
            { _, _, _, _, _, X, _, _, X, _, _, _, X, _, _, _ },
            { _, _, _, X, _, _, _, X, _, X, _, _, _, X, _, _ },
            { _, _, _, X, _, X, X, _, _, _, _, X, _, _, _, X },
            { _, X, _, _, X, _, _, _, X, _, X, _, X, _, X, _ },
            { _, _, _, _, X, _, _, _, _, X, _, X, _, X, _, _ },
            { X, _, _, _, _, X, _, _, _, _, _, X, _, _, X, _ },
            { _, X, _, X, X, _, _, X, _, X, X, _, X, _, _, X },
            { X, _, X, _, _, X, _, _, _, X, _, _, X, X, _, _ },
            { _, _, X, _, _, X, _, X, _, _, _, X, _, _, _, X },
            { X, _, _, _, X, _, _, _, X, _, _, X, _, X, _, _ },
            { _, X, _, _, _, _, X, _, X, _, X, _, _, _, X, _ },
            { _, _, X, X, _, _, _, X, _, _, X, _, _, X, _, _ },
            { X, _, _, _, _, X, X, _, _, X, _, _, X, _, _, X },
            { _, X, _, _, X, _, _, X, X, _, _, X, _, _, _, _ },
            { _, _, _, X, _, _, X, _, _, X, _, _, _, _, _, X }
        };

        const string expectedSolutionStr =
            " ┌──┐  ┌──┐  ┌──┐  ┌────────────────────┐  ┌──┐ \n" +
            " │  │  │  │  │  └──┘  ┌──┐  ┌────────┐  │  │  │ \n" +
            " │  │  │  └──┘  ┌─────┘  │  └─────┐  │  └──┘  │ \n" +
            " │  │  └──┐  ┌──┘  ┌─────┘  ┌─────┘  └────────┘ \n" +
            " │  └─────┘  └──┐  │  ┌──┐  │  ┌──┐  ┌──┐  ┌──┐ \n" +
            " └───────────┐  │  │  │  │  └──┘  └──┘  └──┘  │ \n" +
            " ┌────────┐  └──┘  │  │  │  ┌─────┐  ┌─────┐  │ \n" +
            " └──┐  ┌──┘  ┌──┐  └──┘  └──┘  ┌──┘  └──┐  └──┘ \n" +
            " ┌──┘  └──┐  │  └────────┐  ┌──┘  ┌──┐  └─────┐ \n" +
            " └─────┐  │  └──┐  ┌──┐  │  │  ┌──┘  │  ┌─────┘ \n" +
            " ┌──┐  │  │  ┌──┘  │  │  └──┘  │  ┌──┘  └─────┐ \n" +
            " │  └──┘  │  └─────┘  └──┐  ┌──┘  │  ┌─────┐  │ \n" +
            " └─────┐  └────────┐  ┌──┘  │  ┌──┘  │  ┌──┘  │ \n" +
            " ┌──┐  │  ┌─────┐  └──┘  ┌──┘  │  ┌──┘  └─────┘ \n" +
            " │  └──┘  │  ┌──┘  ┌──┐  └──┐  │  └───────────┐ \n" +
            " └────────┘  └─────┘  └─────┘  └──────────────┘ ";

        var solver = new EverySecondTurnSolver(gridData);
        var solution = solver.GetSolution();
        Assert.NotNull(solution);
        Assert.Equal(expectedSolutionStr, solution.ToString());

        var otherSolution = solver.GetOtherSolution();
        Assert.True(otherSolution == null || otherSolution.Rows == 0);
    }
}