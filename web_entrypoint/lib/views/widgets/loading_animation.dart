import 'package:flutter/material.dart';

class LoadingAnimation extends AnimatedWidget {
  LoadingAnimation({Key key, Animation<double> animation})
      : super(key: key, listenable: animation);

  Widget build(BuildContext context) {
    final animation = listenable as Animation<double>;
    return Center(
      child: Container(
        height: 400,
        width: 400,
        child: CustomPaint(
          painter: LoadingAnimationPainter(animation.value),
        ),
      ),
    );
  }
}

class LoadingAnimationPainter extends CustomPainter {
  final double size;
  LoadingAnimationPainter(this.size);
  // TODO cool animation
  @override
  void paint(Canvas canvas, Size size) {
    var paint = Paint()
      ..color = Colors.yellow
      ..strokeWidth = 5
      ..style = PaintingStyle.fill
      ..strokeCap = StrokeCap.round;
    Offset center = Offset(size.width / 2, size.height / 2);
    canvas.drawCircle(center, this.size, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) {
    return true;
  }
}
