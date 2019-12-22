from seqdiag import parser, builder, drawer

diagram_definition = u"""
   seqdiag {
      browser  -> webserver [label = "GET /index.html"];
      browser <- webserver;
   }
"""
tree = parser.parse_string(diagram_definition)
diagram = builder.ScreenNodeBuilder.build(tree)
draw = drawer.DiagramDraw('PNG', diagram, filename='diagram.png')
draw.draw()
draw.save()
