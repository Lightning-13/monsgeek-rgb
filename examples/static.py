from monsgeek_rgb import create_static_color_packet

packet = create_static_color_packet(255, 0, 0)

print(packet.hex(" "))