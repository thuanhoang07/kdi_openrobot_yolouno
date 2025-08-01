// Khối kiểm tra có target data không
Blockly.Blocks['has_target_data'] = {
  init: function () {
    this.jsonInit({
      type: "has_target_data",
      message0: "Có target data không",
      output: "Boolean",
      colour: "#21c2f3ff",
      tooltip: "Kiểm tra xem có dữ liệu target từ OpenBot hay không",
      helpUrl: ""
    });
  }
};

Blockly.Python['has_target_data'] = function(block) {
  Blockly.Python.definitions_['import_openbot_parser'] = 'from yolouno_phone import OpenBotParser';
  Blockly.Python.definitions_['create_openbot_parser'] = 'parser = OpenBotParser()';
  
  var code = 'parser.is_target_available()';
  return [code, Blockly.Python.ORDER_ATOMIC];
};

// Khối lấy thông tin target
Blockly.Blocks['get_target_info'] = {
  init: function () {
    this.jsonInit({
      type: "get_target_info",
      message0: "Lấy %1 của target",
      args0: [
        {
          type: "field_dropdown",
          name: "PROPERTY",
          options: [
            ["x trung tâm", "x"],
            ["y trung tâm", "y"],
            ["chiều rộng w", "w"],
            ["chiều cao h", "h"]
          ]
        }
      ],
      output: "Number",
      colour: "#21c2f3ff",
      tooltip: "Lấy thông tin target từ OpenBot (x,y là tọa độ trung tâm)",
      helpUrl: ""
    });
  }
};

Blockly.Python['get_target_info'] = function(block) {
  var property = block.getFieldValue('PROPERTY');
  
  Blockly.Python.definitions_['import_openbot_parser'] = 'from yolouno_phone import OpenBotParser';
  Blockly.Python.definitions_['create_openbot_parser'] = 'parser = OpenBotParser()';
  
  var code = 'parser.get_target_' + property + '()';
  return [code, Blockly.Python.ORDER_ATOMIC];
};