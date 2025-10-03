import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import Navbar from "@/components/Navbar";
import {
  Search,
  CheckCircle2,
  Circle,
  Star,
  ChevronLeft,
  ChevronRight,
  RotateCcw,
  Loader2,
} from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { problemsAPI, Problem } from "@/services/api";

const Problems = () => {
  const [difficulty, setDifficulty] = useState("All");
  const [status, setStatus] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Fetch problems from API
  useEffect(() => {
    const fetchProblems = async () => {
      try {
        setLoading(true);
        const data = await problemsAPI.getAllProblems();
        setProblems(data);
        setError(null);
      } catch (err) {
        console.error('Error fetching problems:', err);
        setError('Failed to load problems. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchProblems();
  }, []);

  // Filter problems based on search and filters
  const filteredProblems = problems.filter((problem) => {
    const matchesDifficulty = difficulty === "All" || problem.difficulty === difficulty;
    const matchesSearch = problem.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         problem.topics.some(topic => topic.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesDifficulty && matchesSearch;
  });

  // Calculate stats
  const totalCount = problems.length;
  const solvedCount = 0; // TODO: Get from user progress API
  const progressPercentage = totalCount > 0 ? (solvedCount / totalCount) * 100 : 0;

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "Easy":
        return "bg-green-500/10 text-green-500 border-green-500/20";
      case "Medium":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20";
      case "Hard":
        return "bg-red-500/10 text-red-500 border-red-500/20";
      default:
        return "";
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar isAuthenticated username="CodeMaster" />

      {/* Filter Bar */}
      <div className="sticky top-16 z-40 border-b border-border/50 glass-effect">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="relative flex-1 min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search questions"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-background/50"
              />
            </div>

            <Select defaultValue="all">
              <SelectTrigger className="w-[180px] bg-background/50">
                <SelectValue placeholder="All Topics" />
              </SelectTrigger>
              <SelectContent className="bg-card border-border z-50">
                <SelectItem value="all">All Topics</SelectItem>
                <SelectItem value="array">Array</SelectItem>
                <SelectItem value="string">String</SelectItem>
                <SelectItem value="hash-table">Hash Table</SelectItem>
                <SelectItem value="dynamic-programming">
                  Dynamic Programming
                </SelectItem>
              </SelectContent>
            </Select>

            <div className="flex gap-2">
              {["All", "Easy", "Medium", "Hard"].map((diff) => (
                <Button
                  key={diff}
                  variant={difficulty === diff ? "default" : "outline"}
                  size="sm"
                  onClick={() => setDifficulty(diff)}
                  className={
                    difficulty === diff ? "bg-primary" : "bg-background/50"
                  }
                >
                  {diff}
                </Button>
              ))}
            </div>

            <div className="flex gap-2">
              {["All", "Solved", "Attempted", "Todo"].map((stat) => (
                <Button
                  key={stat}
                  variant={status === stat ? "default" : "outline"}
                  size="sm"
                  onClick={() => setStatus(stat)}
                  className={status === stat ? "bg-primary" : "bg-background/50"}
                >
                  {stat}
                </Button>
              ))}
            </div>

            <Select defaultValue="acceptance">
              <SelectTrigger className="w-[150px] bg-background/50">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent className="bg-card border-border z-50">
                <SelectItem value="acceptance">Acceptance</SelectItem>
                <SelectItem value="frequency">Frequency</SelectItem>
                <SelectItem value="difficulty">Difficulty</SelectItem>
              </SelectContent>
            </Select>

            <Button variant="ghost" size="sm">
              <RotateCcw className="h-4 w-4 mr-2" />
              Reset
            </Button>
          </div>
        </div>
      </div>

      <main className="container mx-auto px-4 py-8 space-y-6">
        {/* Stats Banner */}
        <div className="glass-effect p-6 rounded-lg">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="h-6 w-6 text-primary" />
              <span className="text-2xl font-bold">
                {solvedCount}/{totalCount} Solved
              </span>
            </div>
            <span className="text-muted-foreground">
              {progressPercentage.toFixed(1)}%
            </span>
          </div>
          <Progress value={progressPercentage} className="h-2" />
        </div>

        {/* Loading State */}
        {loading && (
          <div className="glass-effect rounded-lg p-12 flex items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-primary" />
            <span className="ml-3 text-lg">Loading problems...</span>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="glass-effect rounded-lg p-8 text-center">
            <p className="text-red-500 mb-4">{error}</p>
            <Button onClick={() => window.location.reload()}>
              <RotateCcw className="h-4 w-4 mr-2" />
              Retry
            </Button>
          </div>
        )}

        {/* Problems Table */}
        {!loading && !error && (
          <div className="glass-effect rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="border-b border-border/50">
                  <tr className="text-left">
                    <th className="p-4 font-semibold text-sm text-muted-foreground w-20">
                      #
                    </th>
                    <th className="p-4 font-semibold text-sm text-muted-foreground">
                      Title
                    </th>
                    <th className="p-4 font-semibold text-sm text-muted-foreground">
                      Topics
                    </th>
                    <th className="p-4 font-semibold text-sm text-muted-foreground w-32">
                      Acceptance
                    </th>
                    <th className="p-4 font-semibold text-sm text-muted-foreground w-32">
                      Difficulty
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredProblems.length === 0 ? (
                    <tr>
                      <td colSpan={5} className="p-8 text-center text-muted-foreground">
                        No problems found matching your filters.
                      </td>
                    </tr>
                  ) : (
                    filteredProblems.map((problem) => (
                      <tr
                        key={problem.id}
                        className="border-b border-border/30 hover:bg-card/50 transition-colors group"
                      >
                        <td className="p-4 text-muted-foreground">
                          {problem.problem_number}
                        </td>
                        <td className="p-4">
                          <Link
                            to={`/problem/${problem.slug}`}
                            className="hover:text-primary transition-colors font-medium"
                          >
                            {problem.title}
                          </Link>
                        </td>
                        <td className="p-4">
                          <div className="flex gap-1 flex-wrap">
                            {problem.topics.slice(0, 2).map((topic) => (
                              <Badge
                                key={topic}
                                variant="outline"
                                className="text-xs bg-primary/10 border-primary/20"
                              >
                                {topic}
                              </Badge>
                            ))}
                            {problem.topics.length > 2 && (
                              <Badge variant="outline" className="text-xs">
                                +{problem.topics.length - 2}
                              </Badge>
                            )}
                          </div>
                        </td>
                        <td className="p-4 text-muted-foreground">
                          {problem.acceptance_rate.toFixed(1)}%
                        </td>
                        <td className="p-4">
                          <Badge className={getDifficultyColor(problem.difficulty)}>
                            {problem.difficulty}
                          </Badge>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Problems;
