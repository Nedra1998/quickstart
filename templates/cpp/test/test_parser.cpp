#include "parser.hpp"

#include <iostream>

#include "any_type.hpp"
#include "gtest/gtest.h"

class ParserTest : public testing::Test {
 protected:
  virtual void SetUp() {
    p2.AddArgument("--value", "value", cli::Any(3.1415));
    p2.AddArgument(std::vector<std::string>{"-s", "--string"}, "string",
                   cli::Any("Hello World"));
    p2.ArgumentGroup("Sub Group");
    p2.AddArgument("--bool", "bool", "set_true", cli::Any(false),
                   "Boolian flag");
    p2.AddArgument("--reverse", "rev", "set_false", cli::Any(true),
                   "Reverse bool");
  }
  virtual void TearDown() {}
  cli::Parser p1, p2;
};

TEST_F(ParserTest, AddArgument) {
  p1.AddArgument("--test1", "test1");
  p1.AddArgument(std::vector<std::string>{"-t2", "--test2"}, "test2");
  p1.AddArgument("--test3", "test3", cli::Any(3));
  p1.AddArgument(std::vector<std::string>{"-t4", "--test4"}, "test4",
                 cli::Any(4));
  p1.AddArgument("--test5", "test5", "This is test 5");
  p1.ArgumentGroup("Part2");
  p1.AddArgument(std::vector<std::string>{"-t6", "--test6"}, "test6",
                 "This is test 6");
  p1.AddArgument("--test7", "test7", "set_false");
  p1.AddArgument("--test7b", "test7b", "get_value");
  p1.AddArgument(std::vector<std::string>{"-t8", "--test8"}, "test8",
                 "set_true");
  p1.AddArgument("--test9", "test9", "set_true", "This is test 9");
  p1.AddArgument(std::vector<std::string>{"-t10", "--test10"}, "test10",
                 "set_true", "This is test 10");
  p1.AddArgument("--test11", "test11", "set_true", cli::Any(false));
  p1.AddArgument(std::vector<std::string>{"-t12", "--test12"}, "test12",
                 "set_true", cli::Any(false));
  p1.AddArgument("--test13", "test13", "set_false", cli::Any(true),
                 "This is test 13");
  p1.AddArgument(std::vector<std::string>{"-t14", "--test14"}, "test14",
                 "set_false", cli::Any(true), "This is test 14");
  EXPECT_EQ(p1.ArgumentCount(), 15);
  EXPECT_EQ(p1.ArgumentCount("Part2"), 10);
  std::string match =
      "Help Page\n\n\nUsage:  [options]\n\nArguments:\n  --test1           \n  "
      "-t2, --test2      \n  --test3           \n  -t4, --test4      \n  "
      "--test5           This is test 5\n\n  Part2:\n    -t6, --test6    This "
      "is test 6\n    --test7         \n    --test7b        \n    -t8, --test8 "
      "   \n    --test9         This is test 9\n    -t10, --test10  This is "
      "test 10\n    --test11        \n    -t12, --test12  \n    --test13       "
      " This is test 13\n    -t14, --test14  This is test 14\n";
  EXPECT_EQ(p1.HelpString(), match);
}

TEST_F(ParserTest, ParseArgs) {
  const char* arg0[] = {"./ParserTest"};
  p2.SetPrint(true);
  p2.SetVersion("v0.0.0");
  std::map<std::string, cli::Any> out = p2.ParseArgs(1, arg0);
  for (std::map<std::string, cli::Any>::iterator it = out.begin();
       it != out.end(); ++it) {
    std::cout << it->first << ":" << it->second << "\n";
  }
  EXPECT_EQ(out["null"], cli::Any());
  EXPECT_EQ(out["value"], cli::Any(3.1415));
  EXPECT_EQ(out["string"], cli::Any("Hello World"));
  EXPECT_EQ(out["bool"], cli::Any(false));
  EXPECT_EQ(out["rev"], cli::Any(true));
  const char* arg1[] = {"./ParserTest", "--value", "2017"};
  out = p2.ParseArgs(3, arg1);
  EXPECT_EQ(out["null"], cli::Any());
  EXPECT_EQ(out["value"], cli::Any(2017));
  EXPECT_EQ(out["string"], cli::Any("Hello World"));
  EXPECT_EQ(out["bool"], cli::Any(false));
  EXPECT_EQ(out["rev"], cli::Any(true));
  const char* arg2[] = {"./ParserTest", "-s", "Hello There"};
  out = p2.ParseArgs(3, arg2);
  EXPECT_EQ(out["null"], cli::Any());
  EXPECT_EQ(out["value"], cli::Any(3.1415));
  EXPECT_EQ(out["string"], cli::Any(std::string("Hello There")));
  EXPECT_EQ(out["bool"], cli::Any(false));
  EXPECT_EQ(out["rev"], cli::Any(true));
  const char* arg3[] = {"./ParserTest", "--bool"};
  out = p2.ParseArgs(2, arg3);
  EXPECT_EQ(out["null"], cli::Any());
  EXPECT_EQ(out["value"], cli::Any(3.1415));
  EXPECT_EQ(out["string"], cli::Any("Hello World"));
  EXPECT_EQ(out["bool"], cli::Any(true));
  EXPECT_EQ(out["rev"], cli::Any(true));
  const char* arg4[] = {"./ParserTest", "--reverse"};
  out = p2.ParseArgs(2, arg4);
  EXPECT_EQ(out["null"], cli::Any());
  EXPECT_EQ(out["value"], cli::Any(3.1415));
  EXPECT_EQ(out["string"], cli::Any("Hello World"));
  EXPECT_EQ(out["bool"], cli::Any(false));
  EXPECT_EQ(out["rev"], cli::Any(false));
  const char* arg5[] = {"./ParserTest", "--help"};
  out = p2.ParseArgs(2, arg5);
  EXPECT_EQ(out["null"], cli::Any());
  EXPECT_EQ(out["value"], cli::Any(3.1415));
  EXPECT_EQ(out["string"], cli::Any("Hello World"));
  EXPECT_EQ(out["bool"], cli::Any(false));
  EXPECT_EQ(out["rev"], cli::Any(true));
  const char* arg6[] = {"./ParserTest", "--version"};
  out = p2.ParseArgs(2, arg6);
  EXPECT_EQ(out["null"], cli::Any());
  EXPECT_EQ(out["value"], cli::Any(3.1415));
  EXPECT_EQ(out["string"], cli::Any("Hello World"));
  EXPECT_EQ(out["bool"], cli::Any(false));
  EXPECT_EQ(out["rev"], cli::Any(true));
  const char* arg7[] = {"./ParserTest", "--value"};
  p2.ParseArgs(2, arg7);
  const char* arg8[] = {"./ParserTest", "--fake"};
  p2.ParseArgs(2, arg8);
  const char* arg9[] = {"./ParserTest", "--value", "2.7"};
  out = p2.ParseArgs(3, arg9);
  EXPECT_EQ(out["value"], cli::Any(float(2.7)));
  const char* arg10[] = {"./ParserTest", "--value", "2.7.8"};
  out = p2.ParseArgs(3, arg10);
  EXPECT_EQ(out["value"], cli::Any(std::string("2.7.8")));
  const char* arg11[] = {"./ParserTest", "--value", "true"};
  out = p2.ParseArgs(3, arg11);
  EXPECT_EQ(out["value"], cli::Any(true));
  const char* arg12[] = {"./ParserTest", "--value", "false"};
  out = p2.ParseArgs(3, arg12);
  EXPECT_EQ(out["value"], cli::Any(false));
}

TEST_F(ParserTest, SetHelpHeader) {
  std::string match =
      "Custom help header\nWith multiple "
      "lines!\n\n==================\nDont\n\nArguments:\n  --value           "
      "\n  -s, --string      \n\n  Sub Group:\n    --bool          Boolian "
      "flag\n    --reverse       Reverse bool\n";
  p2.SetHelpHeader("Custom help header\nWith multiple lines!");
  p2.SetHelpUsage("Dont");
  EXPECT_EQ(p2.HelpString(), match);
}

TEST_F(ParserTest, SetVersion) {
  p2.SetVersion("v0.0.0");
  EXPECT_EQ(p2.VersionString(), "v0.0.0");
}
