<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="//div[div and (lg or p)]">

<div>

	<xsl:copy-of select="./@*"/>

	<xsl:copy-of select="head"/>

	<div>

		<xsl:attribute name="label">
		<xsl:value-of select="concat(@label, '.0')"/>
		</xsl:attribute>

		<xsl:attribute name="level">
		<xsl:value-of select="@level + 1"/>
		</xsl:attribute>

		<xsl:attribute name="n">
		<xsl:value-of select="0"/>
		</xsl:attribute>

		<xsl:copy-of select="lg|p|pb|lb"/>

	</div>

	<xsl:copy-of select="div"/>

</div>

</xsl:template>

</xsl:stylesheet>