from check_and_publish.src.view import check
import importlib

importlib.reload(check)
if __name__ == '__main__':
    check_view = check.CheckView()
    check_view.run()
