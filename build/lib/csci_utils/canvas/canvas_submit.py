"""Utils for accessing and submitting to Canvas"""
"""Reference: 2021sp-pset-1-cwstoughton-master"""
import canvasapi
from environs import Env
from git import Repo

env = Env()
env.read_env()


class Course_Data:
    """Class that contains relevant data for use in canvasapi."""

    def __init__(self):  # initialize with env vars
        self.course_id = env.int("CANVAS_COURSE_ID")
        self.assignment_id = env.int("CANVAS_ASSIGNMENT_ID")
        self.quiz_id = env.int("CANVAS_QUIZ_ID")
        self.token = env.str("CANVAS_TOKEN")
        self.url = env.str("CANVAS_URL")

    def get_course_info(self):  # get course details from canvas
        self.canvas_root = canvasapi.Canvas(self.url, self.token)
        self.course = self.canvas_root.get_course(self.course_id)
        self.quiz = self.course.get_quiz(self.quiz_id)
        self.assignment = self.course.get_assignment(self.assignment_id)

    def start_quiz(self):  # initiates a quiz attempt and gets questions
        self.quiz_attempt = self.quiz.create_submission()
        self.quiz_questions = self.quiz_attempt.get_submission_questions()

    def show_quiz(
        self,
    ):  # This function is designed to make the quiz human-readable for development purposes
        for Q in self.quiz_questions:
            print("-" * 8)
            print("Question:", Q.question_name)
            print("Type:", Q.question_type)
            print("Text:\n", Q.question_text.split("<p")[1])
            try:
                print("Answer Key:\n", Q.answers)
            except:
                print("Answer Key:\n", Q.answer)
            finally:
                pass

    def quiz_answer_template(
        self,
    ):  # Creates an empty answer data structure for dev use
        template = []
        for i in self.quiz_questions:
            try:
                keys = i.answer
            except:
                keys = i.answers
            answer = {"id": i.id, "answer": keys}
            template.append(answer)
        return template

    def submit_quiz(self, answers):
        self.quiz_attempt.answer_submission_questions(quiz_questions=answers)


def comments(lateDays):
    repo = Repo("", search_parent_directories=True)

    Submission_Comments = dict(
        hexsha=repo.head.commit.hexsha[:8],
        submitted_from=repo.remotes.origin.url,
        dt=repo.head.commit.committed_datetime.isoformat(),
        branch=os.environ.get("TRAVIS_BRANCH", None),  # repo.active_branch.name,
        is_dirty=repo.is_dirty(),
        quiz_submission_id=Canvas.quiz_attempt.id,
        quiz_attempt=Canvas.quiz_attempt.attempt,
        travis_url=os.environ.get("TRAVIS_BUILD_WEB_URL", None),
        use_late_days=lateDays,
    )
    return Submission_Comments


Canvas = Course_Data()
Canvas.get_course_info()
