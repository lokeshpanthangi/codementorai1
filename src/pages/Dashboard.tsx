import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Navbar from "@/components/Navbar";
import {
  Code2,
  CheckCircle2,
  Flame,
  Sparkles,
  Clock,
  Trophy,
  Target,
  Zap,
  Loader2,
} from "lucide-react";
import { 
  AreaChart, 
  Area, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend 
} from "recharts";
import { dailyChallengeAPI, categoriesAPI, problemsAPI, Category, DailyChallenge, Problem } from "@/services/api";
import { useToast } from "@/hooks/use-toast";

const Dashboard = () => {
  const { toast } = useToast();
  const [dailyChallenge, setDailyChallenge] = useState<DailyChallenge | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [recommendedProblems, setRecommendedProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [challenge, cats, allProblems] = await Promise.all([
          dailyChallengeAPI.getTodayChallenge(),
          categoriesAPI.getAllCategories(),
          problemsAPI.getAllProblems()
        ]);
        setDailyChallenge(challenge);
        setCategories(cats);
        // Get first 4 problems as recommended (you can add filtering logic here)
        setRecommendedProblems(allProblems.slice(0, 4));
        setError(null);
      } catch (err: any) {
        const errorMsg = err.response?.data?.detail || err.message || "Failed to load dashboard data";
        setError(errorMsg);
        toast({
          title: "Error loading dashboard",
          description: errorMsg,
          variant: "destructive",
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const progressData = [
    { month: "Jan", easy: 12, medium: 8, hard: 3 },
    { month: "Feb", easy: 15, medium: 10, hard: 4 },
    { month: "Mar", easy: 18, medium: 14, hard: 6 },
    { month: "Apr", easy: 20, medium: 18, hard: 9 },
  ];

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

      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* Hero Card - No Background */}
        <div className="p-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="space-y-2">
              <h1 className="text-3xl md:text-4xl font-bold text-white">
                Welcome back, <span className="text-violet-500">CodeMaster</span>!
              </h1>
              <p className="text-white/70 text-lg">
                "The only way to learn a new programming language is by writing programs in it." - Dennis Ritchie
              </p>
            </div>
            <Button variant="default" size="lg">
              Continue Learning
            </Button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="glass-effect hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Total Problems</p>
                  <p className="text-3xl font-bold">520</p>
                </div>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Code2 className="h-6 w-6 text-primary" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-effect hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Problems Solved</p>
                  <p className="text-3xl font-bold">47</p>
                  <p className="text-sm text-primary">9% completion</p>
                </div>
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <CheckCircle2 className="h-6 w-6 text-primary" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-effect hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Current Streak</p>
                  <p className="text-3xl font-bold">5 days</p>
                </div>
                <div className="h-12 w-12 rounded-lg bg-orange-500/10 flex items-center justify-center">
                  <Flame className="h-6 w-6 text-orange-500" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-effect hover:shadow-lg transition-all duration-300">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">AI Hints Used</p>
                  <p className="text-3xl font-bold">23</p>
                </div>
                <div className="h-12 w-12 rounded-lg bg-purple-500/10 flex items-center justify-center">
                  <Sparkles className="h-6 w-6 text-purple-500" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid - Recommended Questions (Left) and Progress + Daily (Right) */}
        <div className="grid lg:grid-cols-[1fr_400px] gap-6">
          {/* Left: Recommended For You */}
          <Card className="glass-effect">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-primary" />
                Recommended For You 🎯
              </CardTitle>
              <p className="text-sm text-muted-foreground mt-1">Based on your solving patterns</p>
            </CardHeader>
            <CardContent className="space-y-4">
              {loading ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
              ) : recommendedProblems.length > 0 ? (
                recommendedProblems.map((problem, index) => (
                  <Link
                    key={problem.id}
                    to={`/problem/${problem.slug}`}
                    className="block group"
                    style={{ animationDelay: `${index * 100}ms` }}
                  >
                    <div className="p-4 rounded-lg bg-card/30 hover:bg-card/60 border border-border/40 hover:border-primary/40 transition-all duration-300">
                      {/* Top Row: Title and Stats */}
                      <div className="flex items-start justify-between gap-4 mb-3">
                        <div className="flex items-center gap-3 flex-1 min-w-0">
                          {/* Problem Number */}
                          <span className="text-xs font-mono text-muted-foreground whitespace-nowrap">
                            #{problem.problem_number}
                          </span>
                          
                          {/* Title */}
                          <h3 className="font-semibold text-base group-hover:text-primary transition-colors truncate">
                            {problem.title}
                          </h3>
                          
                          {/* Difficulty Badge */}
                          <Badge 
                            className={`${getDifficultyColor(problem.difficulty)} text-xs whitespace-nowrap`}
                          >
                            {problem.difficulty}
                          </Badge>
                        </div>

                        {/* Acceptance Rate */}
                        <div className="flex items-center gap-2 whitespace-nowrap">
                          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-primary/10 border border-primary/20">
                            <Sparkles className="h-3 w-3 text-primary" />
                            <span className="text-xs font-medium text-primary">{problem.acceptance_rate.toFixed(1)}%</span>
                          </div>
                        </div>
                      </div>

                      {/* Category */}
                      <p className="text-sm text-muted-foreground mb-3 pl-8">
                        Category: {problem.category}
                      </p>

                      {/* Tags Row */}
                      <div className="flex items-center gap-2 flex-wrap pl-8">
                        {/* Topic Tags */}
                        {problem.topics.slice(0, 3).map((tag) => (
                          <span
                            key={tag}
                            className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-primary/5 text-primary/90 border border-primary/10 hover:bg-primary/10 hover:border-primary/20 transition-colors cursor-pointer"
                          >
                            {tag}
                          </span>
                        ))}
                        
                        {/* Divider */}
                        {problem.companies.length > 0 && (
                          <>
                            <span className="text-muted-foreground/30">•</span>
                            
                            {/* Company Tags */}
                            {problem.companies.slice(0, 2).map((company) => (
                              <span 
                                key={company}
                                className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-card text-muted-foreground border border-border/50"
                              >
                                {company}
                              </span>
                            ))}
                          </>
                        )}
                      </div>
                    </div>
                  </Link>
                ))
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  No problems available
                </div>
              )}
            </CardContent>
          </Card>

          {/* Right: Progress Chart + Daily Question */}
          <div className="space-y-6">
            {/* Progress Chart - Area Chart */}
            <Card className="glass-effect overflow-hidden">
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Target className="h-4 w-4 text-primary" />
                  Your Progress
                </CardTitle>
                <p className="text-xs text-muted-foreground">Problems solved over time</p>
              </CardHeader>
              <CardContent className="pb-4">
                <ResponsiveContainer width="100%" height={220}>
                  <AreaChart data={progressData}>
                    <defs>
                      <linearGradient id="colorEasy" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(160 84% 39%)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="hsl(160 84% 39%)" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorMedium" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(45 93% 47%)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="hsl(45 93% 47%)" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorHard" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="hsl(0 84% 60%)" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="hsl(0 84% 60%)" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis 
                      dataKey="month" 
                      stroke="hsl(var(--muted-foreground))" 
                      fontSize={11} 
                    />
                    <YAxis 
                      stroke="hsl(var(--muted-foreground))" 
                      fontSize={11} 
                    />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                      }}
                    />
                    <Legend 
                      wrapperStyle={{ fontSize: '11px' }}
                      iconType="circle"
                    />
                    <Area
                      type="monotone"
                      dataKey="easy"
                      stroke="hsl(160 84% 39%)"
                      fillOpacity={1}
                      fill="url(#colorEasy)"
                      strokeWidth={2}
                    />
                    <Area
                      type="monotone"
                      dataKey="medium"
                      stroke="hsl(45 93% 47%)"
                      fillOpacity={1}
                      fill="url(#colorMedium)"
                      strokeWidth={2}
                    />
                    <Area
                      type="monotone"
                      dataKey="hard"
                      stroke="hsl(0 84% 60%)"
                      fillOpacity={1}
                      fill="url(#colorHard)"
                      strokeWidth={2}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            {/* Daily Question - Compact */}
            <Card className="glass-effect">
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-base">
                  <Zap className="h-4 w-4 text-primary" />
                  Daily Challenge
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {loading ? (
                  <div className="flex items-center justify-center py-8">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  </div>
                ) : dailyChallenge ? (
                  <div className="p-4 rounded-lg bg-gradient-to-br from-primary/20 to-primary/5 border border-primary/20 hover:border-primary/40 transition-all duration-300 hover:shadow-lg hover:shadow-primary/20 group">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-base font-bold group-hover:text-primary transition-colors">Problem of the Day</h3>
                      <Badge className={
                        dailyChallenge.problem.difficulty === "Easy"
                          ? "bg-green-500/10 text-green-500 border-green-500/20"
                          : dailyChallenge.problem.difficulty === "Medium"
                          ? "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
                          : "bg-red-500/10 text-red-500 border-red-500/20"
                      }>
                        {dailyChallenge.problem.difficulty}
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-3 group-hover:text-foreground transition-colors">
                      {dailyChallenge.problem.title}
                    </p>
                    <Link to={`/problem/${dailyChallenge.problem.slug}`}>
                      <Button variant="hero" className="w-full group-hover:scale-[1.02] transition-transform" size="sm">
                        Start Solving
                      </Button>
                    </Link>
                  </div>
                ) : (
                  <div className="p-4 rounded-lg bg-muted/50 text-center">
                    <p className="text-sm text-muted-foreground">No daily challenge available</p>
                  </div>
                )}

                <Button variant="outline" className="w-full hover:border-primary/40 hover:bg-primary/5 transition-all duration-300" size="sm">
                  <Trophy className="mr-2 h-4 w-4" />
                  Random Problem
                </Button>

                <div className="grid grid-cols-3 gap-2">
                  <Button variant="ghost" className="flex-col h-auto py-3 hover:bg-green-500/10 hover:border-green-500/30 border border-transparent transition-all duration-300 group">
                    <span className="text-xl font-bold text-green-500 group-hover:scale-110 transition-transform">20</span>
                    <span className="text-xs text-muted-foreground">Easy</span>
                  </Button>
                  <Button variant="ghost" className="flex-col h-auto py-3 hover:bg-yellow-500/10 hover:border-yellow-500/30 border border-transparent transition-all duration-300 group">
                    <span className="text-xl font-bold text-yellow-500 group-hover:scale-110 transition-transform">18</span>
                    <span className="text-xs text-muted-foreground">Medium</span>
                  </Button>
                  <Button variant="ghost" className="flex-col h-auto py-3 hover:bg-red-500/10 hover:border-red-500/30 border border-transparent transition-all duration-300 group">
                    <span className="text-xl font-bold text-red-500 group-hover:scale-110 transition-transform">9</span>
                    <span className="text-xs text-muted-foreground">Hard</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Categories */}
        <div>
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Code2 className="h-6 w-6 text-primary" />
            Browse by Category
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {loading ? (
              <div className="col-span-full flex items-center justify-center py-8">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
              </div>
            ) : categories.length > 0 ? (
              categories.map((category) => (
                <Link key={category.id} to={`/problems?category=${category.slug}`}>
                  <Card className="glass-effect hover:shadow-lg transition-all duration-300 hover:-translate-y-1 cursor-pointer group">
                    <CardContent className="p-6">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-2xl">{category.icon}</span>
                            <h3 className="text-lg font-bold group-hover:text-primary transition-colors">
                              {category.name}
                            </h3>
                          </div>
                          <p className="text-sm text-muted-foreground">{category.problem_count} problems</p>
                          <div className="flex gap-2 mt-2 text-xs">
                            <span className="text-green-500">{category.difficulty_distribution.easy} Easy</span>
                            <span className="text-yellow-500">{category.difficulty_distribution.medium} Med</span>
                            <span className="text-red-500">{category.difficulty_distribution.hard} Hard</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))
            ) : (
              <div className="col-span-full text-center py-8 text-muted-foreground">
                No categories available
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
