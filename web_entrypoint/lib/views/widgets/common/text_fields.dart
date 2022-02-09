import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

Widget _buildTextFieldImpl(TextEditingController controller, String hint,
    Function validator, bool obscure, List formatters) {
  return Padding(
    padding: EdgeInsets.all(8.0),
    child: TextFormField(
      inputFormatters: formatters,
      controller: controller,
      decoration: InputDecoration(
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.blueAccent, width: 3.0),
        ),
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(color: Colors.grey, width: 3.0),
        ),
        hintText: hint,
      ),
      validator: validator,
      obscureText: obscure,
    ),
  );
}

Widget buildUnsignedIntField(TextEditingController controller, String hint,
    {bool obscure = false}) {
  return _buildTextFieldImpl(controller, hint, (value) => null, obscure,
      <TextInputFormatter>[FilteringTextInputFormatter.digitsOnly]);
}

Widget buildTextField(TextEditingController controller, String hint,
    {bool obscure = false}) {
  return _buildTextFieldImpl(
      controller, hint, (value) => null, obscure, <TextInputFormatter>[]);
}

Widget buildValidatedTextField(
    TextEditingController controller, String hint, Function validator,
    {bool obscure = false}) {
  if (validator == null) {
    validator = (value) {
      if (value.isEmpty) {
        return "Please enter $hint";
      }
      return null;
    };
  }
  return _buildTextFieldImpl(
      controller, hint, validator, obscure, <TextInputFormatter>[]);
}
