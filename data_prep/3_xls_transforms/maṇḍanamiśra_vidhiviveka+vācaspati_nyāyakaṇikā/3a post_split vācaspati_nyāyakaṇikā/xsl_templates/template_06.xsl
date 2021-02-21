<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="p">
<p>
	<xsl:copy-of select="./@*"/>

	<xsl:variable name="curr_pb_n" select="@pb_n"/>
	<xsl:attribute name="pb_n2">
	<xsl:value-of select="count(preceding-sibling::p[@pb_n=$curr_pb_n])+1"/>
	</xsl:attribute>

	<xsl:copy-of select="./node()[not(self::pb)]"/>
</p>
</xsl:template>

</xsl:stylesheet>