# DNR - A News Recommendation System Based on Deep Learning
![Static Badge](https://img.shields.io/badge/python-3.6-orange?style=flat-square) ![Static Badge](https://img.shields.io/badge/%20flask-2.0.3-orange?style=flat-square) ![Static Badge](https://img.shields.io/badge/%20Neural%20Network-TextCNN-orange?style=flat-square)

This is my graduation project, and I know there are some issues with it, but I still hope it can help you.

## Quick start

This is how you set up an development instance of DNR:

- Create a virtual environment

  ```
  conda create --name <env-name> python=3.6
  ```

- Enter this virtual environment

  ```
  conda activate <env-name>
  ```

- Install the requirements.txt

  ```
  pip install requirements.txt
  ```

- Run server

  > Guys, if you don't connect to MySQL database, you can't login it. Maybe you should see the next chapter which is Database Setting.

  ```
  python manager.py runserver
  ```

## Database Setting

When you first use the system, you should properly configure MySQL related configurations to ensure that the code can connect to the database. In the path which is `config/local_setting.py`, you should modify `SQLALCHEMY_DATABASE_URI`. Then run the server, your username is root and password is 123456. 

## License

This project is licensed under the [GPL-2.0 license](https://github.com/chaoql/DNR/blob/main/LICENSE).

## Links

[my blog]: https://blog.csdn.net/qq_43510916?type=blog

